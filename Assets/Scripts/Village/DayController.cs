using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    // Làng ban ngày kiểu Stardew: đi lại bằng WASD, đến trước cửa bấm E để làm việc (mỗi việc 1 lượt), tối đến điện để đi đêm.
    // Gắn vào object Battle đang có: Add Component → DayController. Bấm Play là vào ngày 1.
    // Map, nhà cửa, va chạm: Assets/Resources/World/ (sinh bằng ArtSource/draw_world.py). Sprite đi: Resources/Walk/.
    [RequireComponent(typeof(BattleController))]
    public class DayController : MonoBehaviour
    {
        [SerializeField] VillageConfig config;
        [SerializeField] float walkSpeed = 80f;      // pixel map mỗi giây
        [SerializeField] float interactRange = 18f;  // đứng cách cửa bao xa thì bấm E được

        enum Panel { None, Home, Field, Dinh, Npc, Clue, Night, Leader, Map }

        static readonly string[] NightNames = { "Trận 1 · Ma đói, Ma nước", "Trận 2 · Ma nhện, Ma đói" };
        static readonly string[] Dirs = { "down", "up", "left", "right" };

        BattleController battle;
        VillageState state;
        VillageMap map;
        Panel panel = Panel.None;
        MapSpot openSpot;
        string clueFriend;
        int homeTab;           // 0 nấu ăn, 1 làm đồ, 2 người đi
        bool bagOpen;
        bool atNight;
        Rect panelRect, bagRect;
        readonly Dictionary<string, Texture2D> texCache = new Dictionary<string, Texture2D>();

        // người chơi
        string leader;         // người đang đi lại trên map
        Vector2 pos;           // vị trí chân, pixel map
        int facing;            // 0 xuống, 1 lên, 2 trái, 3 phải
        float walkT;
        bool moving;
        bool askLeader = true; // sáng nào cũng hỏi ai đi
        readonly HashSet<KeyCode> held = new HashSet<KeyCode>();

        // camera
        int k = 3;             // số pixel màn hình cho 1 pixel map (luôn nguyên để pixel nét)
        Vector2 cam;           // góc trên trái tầm nhìn, pixel map
        Vector2 worldOff;      // dời map vào giữa khi màn hình rộng hơn map

        // tương tác
        MapSpot nearSpot;
        MapFriend nearFriend;

        GUIStyle title, text, small, dim, right, header, gold, label, tip;
        GUIStyle panelSt, btn, tabOn, plaqueSt, tipSt;

        static readonly Color Gold = new Color(1f, 0.85f, 0.3f);
        static readonly Color Off = new Color(0.3f, 0.3f, 0.32f);
        static readonly Color Cream = new Color(0.93f, 0.89f, 0.77f);

        struct Drawable
        {
            public float b;          // đáy, để xếp trước sau
            public Texture2D tex;
            public Rect world;       // khung trên map
            public Rect uv;
            public float alpha;
            public bool shadow;      // bóng tròn dưới chân
        }

        readonly List<Drawable> drawList = new List<Drawable>();

        void Awake()
        {
            battle = GetComponent<BattleController>();
            battle.autoStart = false;
            battle.OnFinished = OnNightEnd;
            if (config == null) config = VillageConfig.CreateDefault();
            state = new VillageState(config);
            map = VillageMap.Load();
            leader = config.friends.Count > 0 ? config.friends[0] : "Minh";
            WakeUp();
        }

        void WakeUp()
        {
            pos = new Vector2(map.spawn.x, map.spawn.y);
            facing = 0;
            askLeader = true;
        }

        void OnApplicationFocus(bool focus)
        {
            if (!focus) held.Clear();
        }

        // ---------- đêm ----------

        void GoNight(int shrine)
        {
            atNight = true;
            panel = Panel.None;
            bagOpen = false;
            held.Clear();
            battle.StartBattle(state.BagForNight(), shrine, state.TonightBonusHp);
        }

        void OnNightEnd(bool won, Dictionary<string, int> left)
        {
            atNight = false;
            state.AfterNight(won, left);
            WakeUp();
        }

        // ---------- đi lại ----------

        bool Held(KeyCode a, KeyCode b)
        {
            return held.Contains(a) || held.Contains(b);
        }

        void Update()
        {
            if (atNight || !map.Loaded) return;
            if (panel != Panel.None)
            {
                moving = false;
                return;
            }
            float mx = 0, my = 0;
            if (Held(KeyCode.A, KeyCode.LeftArrow)) mx -= 1;
            if (Held(KeyCode.D, KeyCode.RightArrow)) mx += 1;
            if (Held(KeyCode.W, KeyCode.UpArrow)) my -= 1;
            if (Held(KeyCode.S, KeyCode.DownArrow)) my += 1;
            moving = mx != 0 || my != 0;
            if (!moving)
            {
                walkT = 0;
                return;
            }
            var v = new Vector2(mx, my).normalized * walkSpeed * Mathf.Min(Time.deltaTime, 0.05f);
            TryMove(new Vector2(v.x, 0));
            TryMove(new Vector2(0, v.y));
            if (mx != 0) facing = mx < 0 ? 2 : 3;
            else facing = my < 0 ? 1 : 0;
            walkT += Time.deltaTime;
        }

        // Hộp va chạm ở chân: rộng 10, cao 4 pixel.
        bool Blocked(Vector2 p)
        {
            for (float x = -5; x <= 5; x += 2.5f)
                if (map.Solid(p.x + x, p.y) || map.Solid(p.x + x, p.y - 3)) return true;
            return false;
        }

        void TryMove(Vector2 d)
        {
            var n = pos + d;
            if (!Blocked(n)) pos = n;
        }

        void FindNearby()
        {
            nearSpot = null;
            nearFriend = null;
            float best = interactRange;
            foreach (var sp in map.spots)
            {
                float d;
                if (sp.kind == "field")
                    d = new Rect(sp.x - 4, sp.y - 4, sp.w + 8, sp.h + 8).Contains(pos) ? 0f : 999f;
                else
                    d = Vector2.Distance(pos, new Vector2(sp.dx, sp.dy));
                if (d <= best)
                {
                    best = d;
                    nearSpot = sp;
                }
            }
            foreach (var f in map.friends)
            {
                if (f.name == leader) continue;
                float d = Vector2.Distance(pos, new Vector2(f.x, f.y + 4));
                if (d <= best)
                {
                    best = d;
                    nearSpot = null;
                    nearFriend = f;
                }
            }
        }

        string PromptText()
        {
            if (nearFriend != null) return "Nói chuyện với " + nearFriend.name;
            if (nearSpot == null) return null;
            switch (nearSpot.kind)
            {
                case "home": return "Vào nhà";
                case "field": return "Làm ruộng";
                case "dinh": return "Sửa đình";
                case "npc": return "Thăm " + nearSpot.npc;
                case "shrine": return "Đi đêm · " + nearSpot.name;
                default: return nearSpot.name + " (chưa mở)";
            }
        }

        void Interact()
        {
            if (nearFriend != null)
            {
                clueFriend = nearFriend.name;
                openSpot = null;
                panel = Panel.Clue;
                return;
            }
            if (nearSpot == null) return;
            openSpot = nearSpot;
            switch (nearSpot.kind)
            {
                case "home": panel = Panel.Home; break;
                case "field": panel = Panel.Field; break;
                case "dinh": panel = Panel.Dinh; break;
                case "npc": panel = Panel.Npc; break;
                case "shrine": panel = Panel.Night; break;
                default:
                    state.Log.Add(nearSpot.name + ": sương dày đặc, chưa vào được.");
                    openSpot = null;
                    break;
            }
        }

        void Close()
        {
            panel = Panel.None;
            openSpot = null;
        }

        void HandleKeys()
        {
            var ev = Event.current;
            if (ev.type == EventType.KeyUp)
            {
                held.Remove(ev.keyCode);
                return;
            }
            if (ev.type != EventType.KeyDown || ev.keyCode == KeyCode.None) return;
            held.Add(ev.keyCode);
            var kc = ev.keyCode;
            if (kc == KeyCode.Escape)
            {
                if (panel != Panel.None) Close();
                else bagOpen = false;
                ev.Use();
            }
            else if (kc == KeyCode.B)
            {
                bagOpen = !bagOpen;
                ev.Use();
            }
            else if (kc == KeyCode.M || kc == KeyCode.Tab)
            {
                if (panel == Panel.Map) Close();
                else if (panel == Panel.None) panel = Panel.Map;
                ev.Use();
            }
            else if (panel == Panel.None && (kc == KeyCode.E || kc == KeyCode.Space || kc == KeyCode.Return || kc == KeyCode.KeypadEnter))
            {
                Interact();
                ev.Use();
            }
        }

        // ---------- UI ----------

        void OnGUI()
        {
            if (atNight) return;
            EnsureStyles();
            HandleKeys();
            if (!map.Loaded)
            {
                GUI.Label(new Rect(20, 20, Screen.width - 40, 60), "Thiếu map: chạy ArtSource/draw_world.py để sinh Assets/Resources/World/.", title);
                return;
            }
            if (askLeader && panel == Panel.None)
            {
                askLeader = false;
                panel = Panel.Leader;
            }
            if (panel == Panel.None) FindNearby();
            else { nearSpot = null; nearFriend = null; }

            // Thế giới: vẽ theo pixel màn hình, tỉ lệ nguyên.
            GUI.matrix = Matrix4x4.identity;
            k = Mathf.Max(1, Mathf.RoundToInt(Screen.height / 270f));
            float viewW = Screen.width / (float)k, viewH = Screen.height / (float)k;
            cam.x = map.width <= viewW ? 0 : Mathf.Clamp(pos.x - viewW / 2f, 0, map.width - viewW);
            cam.y = map.height <= viewH ? 0 : Mathf.Clamp(pos.y - 12 - viewH / 2f, 0, map.height - viewH);
            cam = new Vector2(Mathf.Round(cam.x), Mathf.Round(cam.y));
            worldOff = new Vector2(map.width < viewW ? (viewW - map.width) / 2f : 0, map.height < viewH ? (viewH - map.height) / 2f : 0);
            if (Event.current.type == EventType.Repaint) // thế giới không có nút bấm: chỉ vẽ ở lượt Repaint
            {
                Square(new Rect(0, 0, Screen.width, Screen.height), new Color(0.12f, 0.17f, 0.11f));
                DrawWorld();
                DrawPrompt();
            }

            // Giao diện: toạ độ ảo cao 720.
            float s = Screen.height / 720f;
            GUI.matrix = Matrix4x4.Scale(new Vector3(s, s, 1f));
            float w = Screen.width / s;
            DrawHud(w);
            DrawMinimap(w);
            if (bagOpen) DrawBag(w);
            if (panel == Panel.Map) DrawBigMap(w);
            else if (panel != Panel.None) DrawOpenPanel(w);
            DrawLog(w);
        }

        // Pixel map → pixel màn hình.
        Rect ScreenRect(float x, float y, float ww, float hh)
        {
            return new Rect((Mathf.Round(x) - cam.x + worldOff.x) * k, (Mathf.Round(y) - cam.y + worldOff.y) * k, ww * k, hh * k);
        }

        void DrawWorld()
        {
            GUI.DrawTexture(ScreenRect(0, 0, map.width, map.height), map.ground);
            var water = Tex("World/water_" + (int)(Time.time / 0.45f) % 3);
            if (water != null) GUI.DrawTexture(ScreenRect(0, 0, map.width, map.height), water);

            float viewW = Screen.width / (float)k, viewH = Screen.height / (float)k;
            var view = new Rect(cam.x - worldOff.x - 8, cam.y - worldOff.y - 8, viewW + 16, viewH + 16);
            var playerBox = new Rect(pos.x - 10, pos.y - 34, 20, 34);
            drawList.Clear();

            float aw = map.atlas.width, ah = map.atlas.height;
            foreach (var o in map.objects)
            {
                var wr = new Rect(o.x, o.y, o.w, o.h);
                if (!wr.Overlaps(view)) continue;
                bool behind = o.fade && o.b > pos.y && wr.Overlaps(playerBox);
                drawList.Add(new Drawable
                {
                    b = o.b, tex = map.atlas, world = wr,
                    uv = new Rect(o.ax / aw, 1f - (o.ay + o.h) / ah, o.w / aw, o.h / ah),
                    alpha = behind ? 0.45f : 1f
                });
            }
            AddCrops(view);
            foreach (var f in map.friends)
            {
                if (f.name == leader) continue;
                int dir = 0;
                var toPlayer = pos - new Vector2(f.x, f.y);
                if (toPlayer.magnitude < 56f) // quay sang nhìn người chơi khi lại gần
                    dir = Mathf.Abs(toPlayer.x) > Mathf.Abs(toPlayer.y) ? (toPlayer.x < 0 ? 2 : 3) : (toPlayer.y < 0 ? 1 : 0);
                AddActor(f.name, dir, 0, new Vector2(f.x, f.y));
            }
            int frame = moving ? new[] { 1, 0, 2, 0 }[(int)(walkT * 8f) % 4] : 0;
            AddActor(leader, facing, frame, pos);

            drawList.Sort((a, b) => a.b.CompareTo(b.b));
            var old = GUI.color;
            foreach (var d in drawList)
            {
                if (d.shadow)
                {
                    GUI.color = new Color(0f, 0f, 0f, 0.28f);
                    GUI.DrawTexture(ScreenRect(d.world.x + 3, d.b - 2, 10, 3), Texture2D.whiteTexture);
                }
                GUI.color = new Color(1f, 1f, 1f, d.alpha);
                var sr = ScreenRect(d.world.x, d.world.y, d.world.width, d.world.height);
                if (d.uv.width > 0) GUI.DrawTextureWithTexCoords(sr, d.tex, d.uv);
                else GUI.DrawTexture(sr, d.tex);
            }
            GUI.color = old;

            DrawSmoke();
            DrawShrineFx();
            DrawCloudShadows();
            DrawDaylight();
        }

        void AddActor(string name, int dir, int frame, Vector2 feet)
        {
            var tex = Tex("Walk/" + BattleController.SpriteKey(name) + "_" + Dirs[dir] + "_" + frame);
            if (tex == null) return;
            drawList.Add(new Drawable
            {
                b = feet.y, tex = tex, world = new Rect(feet.x - tex.width / 2f, feet.y - tex.height + 1, tex.width, tex.height),
                alpha = 1f, shadow = true
            });
        }

        // Cây trên ruộng theo trạng thái từng ô: mầm, đang lớn, chín.
        void AddCrops(Rect view)
        {
            int n = Mathf.Min(state.Plots.Count, map.plots.Length);
            for (int i = 0; i < n; i++)
            {
                var p = state.Plots[i];
                if (p.crop < 0) continue;
                var pr = map.plots[i];
                if (!new Rect(pr.x, pr.y, pr.w, pr.h).Overlaps(view)) continue;
                var cd = config.crops[p.crop];
                bool ready = state.IsReady(i);
                float grown = 1f - (float)state.DaysLeft(i) / cd.days;
                int stage = ready ? 2 : (grown < 0.4f ? 0 : 1);
                var tex = Tex("World/crop_" + BattleController.SpriteKey(cd.name) + "_" + stage);
                if (tex == null) continue;
                const int cell = 14;
                int cols = pr.w / cell, rows = pr.h / cell;
                for (int cy = 0; cy < rows; cy++)
                for (int cx = 0; cx < cols; cx++)
                {
                    float x = pr.x + cx * cell + (pr.w - cols * cell) / 2f + (cell - tex.width) / 2f;
                    float bottom = pr.y + cy * cell + (pr.h - rows * cell) / 2f + cell;
                    drawList.Add(new Drawable
                    {
                        b = bottom, tex = tex, world = new Rect(x, bottom - tex.height + 2, tex.width, tex.height), alpha = 1f
                    });
                }
            }
        }

        void MapPixel(float x, float y, float size, Color c)
        {
            Square(ScreenRect(x, y, Mathf.Round(size), Mathf.Round(size)), c);
        }

        void DrawSmoke()
        {
            const int puffs = 7;
            foreach (var s in map.smoke)
                for (int i = 0; i < puffs; i++)
                {
                    float t = Mathf.Repeat(Time.time * 0.3f + (float)i / puffs, 1f);
                    float x = s.x + t * 10f + Mathf.Sin(t * 7f + i) * 1.5f;
                    float y = s.y - t * 26f;
                    float size = 2f + t * 3f;
                    MapPixel(x - size / 2f, y - size / 2f, size, new Color(0.86f, 0.86f, 0.84f, 0.55f * (1f - t)));
                }
        }

        // Sương tím quanh điện có thực thể bám; sương trắng chắn điện chưa mở.
        void DrawShrineFx()
        {
            var fog = Tex("World/fog");
            if (fog == null) return;
            var old = GUI.color;
            foreach (var sp in map.spots)
            {
                if (sp.kind == "shrine")
                {
                    GUI.color = new Color(0.55f, 0.42f, 0.7f, 0.16f + 0.1f * Mathf.Sin(Time.time * 1.3f));
                    GUI.DrawTexture(ScreenRect(sp.x - 30 + Mathf.Sin(Time.time * 0.5f) * 6f, sp.y + sp.h * 0.35f, sp.w + 60, sp.h * 0.8f), fog);
                }
                else if (sp.kind == "locked")
                {
                    GUI.color = new Color(1f, 1f, 1f, 0.85f);
                    float top = Mathf.Min(sp.y, sp.dy - 30);
                    float bottom = Mathf.Max(sp.y + sp.h, sp.dy - 4);
                    GUI.DrawTexture(ScreenRect(sp.x - 18, top - 6, sp.w + 36, bottom - top + 12), fog);
                    var lk = Tex("World/lock");
                    GUI.color = Color.white;
                    if (lk != null) GUI.DrawTexture(ScreenRect(sp.dx - lk.width / 2f, sp.dy - 26, lk.width, lk.height), lk);
                }
            }
            GUI.color = old;
        }

        void DrawCloudShadows()
        {
            var cloud = Tex("World/cloud");
            if (cloud == null) return;
            var old = GUI.color;
            GUI.color = new Color(0.05f, 0.08f, 0.12f, 0.12f);
            float span = map.width + 300;
            for (int i = 0; i < 3; i++)
            {
                float x = Mathf.Repeat(Time.time * 5f + i * span / 3f, span) - 220f;
                float y = 80f + i * 190f;
                GUI.DrawTexture(ScreenRect(x, y, cloud.width * 2, cloud.height * 2), cloud);
            }
            GUI.color = old;
        }

        // Nắng ngả theo số lượt đã dùng: sáng → trưa → chiều → chạng vạng.
        void DrawDaylight()
        {
            int used = config.actionsPerDay - state.ActionsLeft;
            float t = (float)used / Mathf.Max(1, config.actionsPerDay);
            Color c = state.ActionsLeft <= 0
                ? new Color(0.28f, 0.18f, 0.42f, 0.28f)
                : new Color(1f, 0.55f - 0.15f * t, 0.2f, 0.16f * t * t);
            Square(new Rect(0, 0, Screen.width, Screen.height), c);
        }

        string TimeOfDay()
        {
            switch (state.ActionsLeft)
            {
                case 0: return "Chạng vạng";
                case 1: return "Chiều tà";
                case 2: return "Chiều";
                case 3: return "Trưa";
                default: return "Sáng";
            }
        }

        // Gợi ý [E] nổi trên đầu người chơi.
        void DrawPrompt()
        {
            string p = PromptText();
            if (p == null) return;
            var head = ScreenRect(pos.x, pos.y - 40, 0, 0);
            var content = new GUIContent("E  " + p);
            var size = label.CalcSize(content);
            float bob = Mathf.Round(Mathf.Sin(Time.time * 5f)) * 2f;
            var r = new Rect(head.x - size.x / 2f - 12, head.y - size.y - 12 + bob, size.x + 24, size.y + 10);
            if (plaqueSt != null) GUI.Box(r, GUIContent.none, plaqueSt);
            else Square(r, new Color(0.07f, 0.06f, 0.09f, 0.85f));
            var key = new Rect(r.x + 8, r.y + 4, 16, size.y + 2);
            Square(key, Gold);
            var old = label.normal.textColor;
            label.normal.textColor = new Color(0.15f, 0.1f, 0.05f);
            GUI.Label(new Rect(key.x + 3, key.y, 14, size.y), "E", label);
            label.normal.textColor = nearSpot != null && nearSpot.kind == "locked" ? new Color(0.65f, 0.65f, 0.7f) : Cream;
            GUI.Label(new Rect(r.x + 30, r.y + 5, size.x, size.y), p, label);
            label.normal.textColor = old;
        }

        NpcDef FindNpc(string name)
        {
            return config.npcs.Find(n => n.name == name);
        }

        // ---------- HUD ----------

        void DrawHud(float w)
        {
            var card = new Rect(16, 12, 340, 96);
            Box(card);
            var sun = Tex("World/sun");
            if (sun != null) GUI.DrawTexture(new Rect(card.x + 14, card.y + 16 + Mathf.Round(Mathf.Sin(Time.time * 2f)) * 2f,
                sun.width * 2, sun.height * 2), sun);
            ShadowLabel(new Rect(card.x + 60, card.y + 10, 270, 28), "Ngày " + state.Day + "/" + config.loopDays + " · " + TimeOfDay(), title);
            GUI.Label(new Rect(card.x + 60, card.y + 40, 120, 22), "Vòng lặp " + state.Loop, small);
            GUI.Label(new Rect(card.x + 164, card.y + 40, 50, 22), "Lượt", small);
            for (int i = 0; i < config.actionsPerDay; i++)
            {
                var pip = new Rect(card.x + 204 + i * 24, card.y + 43, 16, 16);
                Square(pip, new Color(0.08f, 0.06f, 0.06f));
                Square(new Rect(pip.x + 2, pip.y + 2, 12, 12), i < state.ActionsLeft ? Gold : Off);
                if (i < state.ActionsLeft) Square(new Rect(pip.x + 2, pip.y + 2, 12, 4), new Color(1f, 0.95f, 0.7f));
            }
            string line = state.TonightBonusHp > 0 ? "Đã ăn: +" + state.TonightBonusHp + " HP tối đa đêm nay"
                : state.CanAct ? "Đang đi: " + leader : "Hết lượt. Đến Điện Thoải phủ để đi đêm.";
            GUI.Label(new Rect(card.x + 60, card.y + 64, 280, 22), line, state.CanAct && state.TonightBonusHp == 0 ? dim : gold);

            var hint = new Rect(w - 452, 664, 436, 42);
            if (plaqueSt != null) GUI.Box(hint, GUIContent.none, plaqueSt);
            GUI.Label(new Rect(hint.x + 12, hint.y + 4, hint.width - 24, 20), "WASD / mũi tên: đi · E: tương tác", small);
            GUI.Label(new Rect(hint.x + 12, hint.y + 21, hint.width - 24, 20), "B: túi đồ · M: bản đồ · Esc: đóng", small);
        }

        void DrawLog(float w)
        {
            var r = new Rect(16, 650, w - 484, 62);
            if (plaqueSt != null) GUI.Box(r, GUIContent.none, plaqueSt);
            else Square(r, new Color(0.07f, 0.06f, 0.09f, 0.8f));
            int count = Mathf.Min(3, state.Log.Count);
            for (int i = 0; i < count; i++)
                GUI.Label(new Rect(r.x + 12, r.y + 6 + i * 17, r.width - 24, 18), state.Log[state.Log.Count - count + i],
                    i == count - 1 ? small : dim);
        }

        // Bản đồ nhỏ góc phải trên: nền map, chấm người chơi, chấm điện.
        void DrawMinimap(float w)
        {
            const float mw = 216;
            float mh = mw * map.height / map.width;
            var frame = new Rect(w - mw - 28, 12, mw + 12, mh + 12);
            Box(frame);
            var r = new Rect(frame.x + 6, frame.y + 6, mw, mh);
            DrawMapImage(r);
            float sx = mw / map.width;
            float blink = Mathf.Repeat(Time.time, 0.8f) < 0.5f ? 1f : 0.4f;
            foreach (var sp in map.spots)
                if (sp.kind == "shrine")
                    Square(new Rect(r.x + sp.dx * sx - 3, r.y + sp.dy * sx - 3, 6, 6), new Color(0.75f, 0.5f, 1f));
            Square(new Rect(r.x + pos.x * sx - 3, r.y + pos.y * sx - 3, 6, 6), new Color(1f, 1f, 1f, blink));
            Outline(new Rect(r.x + pos.x * sx - 4, r.y + pos.y * sx - 4, 8, 8), new Color(0.1f, 0.05f, 0.05f, blink), 1f);
        }

        void DrawMapImage(Rect r)
        {
            GUI.DrawTexture(r, Tex("World/minimap") ?? map.ground); // ảnh ghép sẵn nền + nhà cửa
        }

        // Bản đồ lớn (M): tên từng nơi.
        void DrawBigMap(float w)
        {
            Square(new Rect(0, 0, w, 720), new Color(0f, 0f, 0f, 0.55f));
            float mh = 560, mw = mh * map.width / map.height;
            var frame = new Rect((w - mw) / 2f - 10, 60, mw + 20, mh + 20);
            Box(frame);
            var r = new Rect(frame.x + 10, frame.y + 10, mw, mh);
            DrawMapImage(r);
            float sx = mw / map.width;
            foreach (var sp in map.spots)
            {
                var size = label.CalcSize(new GUIContent(sp.name));
                var lr = new Rect(r.x + (sp.x + sp.w / 2f) * sx - size.x / 2f - 8, r.y + (sp.y + sp.h) * sx + 2, size.x + 16, size.y + 6);
                if (plaqueSt != null) GUI.Box(lr, GUIContent.none, plaqueSt);
                var old = label.normal.textColor;
                if (sp.kind == "locked") label.normal.textColor = new Color(0.62f, 0.62f, 0.68f);
                GUI.Label(new Rect(lr.x + 8, lr.y + 3, size.x, size.y), sp.name, label);
                label.normal.textColor = old;
            }
            float blink = Mathf.Repeat(Time.time, 0.8f) < 0.5f ? 1f : 0.4f;
            Square(new Rect(r.x + pos.x * sx - 5, r.y + pos.y * sx - 5, 10, 10), new Color(1f, 1f, 1f, blink));
            ShadowLabel(new Rect(frame.x, 24, frame.width, 30), "Bản đồ làng  ·  M hoặc Esc để đóng", title);
        }

        void DrawBag(float w)
        {
            bagRect = new Rect(w - 356, 180, 340, 460);
            Box(bagRect);
            ShadowLabel(new Rect(bagRect.x + 16, bagRect.y + 12, bagRect.width, 26), "Túi đồ", title);
            float y = bagRect.y + 46;
            var keys = new List<string>(state.Inv.Keys);
            keys.Sort();
            foreach (var key in keys)
            {
                int n = state.Count(key);
                if (n <= 0) continue;
                var ic = Icon(key);
                if (ic != null) GUI.DrawTexture(new Rect(bagRect.x + 16, y, 28, 28), ic, ScaleMode.ScaleToFit);
                else Square(new Rect(bagRect.x + 24, y + 10, 10, 10), new Color(0.55f, 0.5f, 0.4f));
                GUI.Label(new Rect(bagRect.x + 54, y + 4, bagRect.width - 120, 22), key, text);
                GUI.Label(new Rect(bagRect.xMax - 72, y + 4, 56, 22), "x" + n, right);
                y += 32;
                if (y > bagRect.yMax - 34) break;
            }
            GUI.Label(new Rect(bagRect.x + 16, bagRect.yMax - 30, bagRect.width - 28, 22), "Bùa và thuốc tự mang theo khi đi đêm.", dim);
        }

        // ---------- bảng thao tác ----------

        float PanelHeight()
        {
            switch (panel)
            {
                case Panel.Home: return homeTab == 0 ? 250 : homeTab == 1 ? 500 : 330;
                case Panel.Field: return 400;
                case Panel.Dinh: return 380;
                case Panel.Npc: return 300;
                case Panel.Clue: return 250;
                case Panel.Leader: return 320;
                default: return 120 + NightNames.Length * 56;
            }
        }

        string PanelTitle()
        {
            switch (panel)
            {
                case Panel.Clue: return clueFriend;
                case Panel.Night: return "Đi đêm";
                case Panel.Leader: return "Ngày " + state.Day + ". Hôm nay ai đi?";
                case Panel.Npc: return openSpot.name + " · " + openSpot.npc;
                default: return openSpot != null ? openSpot.name : "";
            }
        }

        void DrawOpenPanel(float w)
        {
            const float pw = 660;
            float ph = PanelHeight();
            float x = (w - pw) / 2f;
            if (bagOpen) x = Mathf.Min(x, w - 356 - 16 - pw);
            panelRect = new Rect(Mathf.Max(16, x), Mathf.Max(70, (720 - ph) / 2f - 20), pw, ph);
            Box(panelRect);
            ShadowLabel(new Rect(panelRect.x + 20, panelRect.y + 14, pw - 150, 28), PanelTitle(), title);
            Square(new Rect(panelRect.x + 16, panelRect.y + 44, pw - 32, 2), new Color(0.73f, 0.56f, 0.27f, 0.5f));
            if (Btn(new Rect(panelRect.xMax - 116, panelRect.y + 10, 100, 30), "Đóng (Esc)")) { Close(); return; }

            var inner = new Rect(panelRect.x + 18, panelRect.y + 54, pw - 36, ph - 66);
            switch (panel)
            {
                case Panel.Home: DrawHome(inner); break;
                case Panel.Field: DrawField(inner); break;
                case Panel.Dinh: DrawDinh(inner); break;
                case Panel.Npc: DrawNpc(inner, FindNpc(openSpot.npc)); break;
                case Panel.Clue: DrawClue(inner); break;
                case Panel.Night: DrawNightPick(inner); break;
                case Panel.Leader: DrawLeaderPick(inner); break;
            }

            var ev = Event.current;
            if (ev.type == EventType.MouseDown && !panelRect.Contains(ev.mousePosition) && !(bagOpen && bagRect.Contains(ev.mousePosition)))
            {
                Close();
                ev.Use();
            }
        }

        void DrawHome(Rect r)
        {
            if (Tab(new Rect(r.x, r.y, 150, 34), "Nấu ăn", homeTab == 0)) homeTab = 0;
            if (Tab(new Rect(r.x + 158, r.y, 150, 34), "Làm đồ", homeTab == 1)) homeTab = 1;
            if (Tab(new Rect(r.x + 316, r.y, 150, 34), "Người đi", homeTab == 2)) homeTab = 2;
            var body = new Rect(r.x, r.y + 46, r.width, r.height - 46);
            if (homeTab == 2) DrawLeaderPick(body);
            else DrawRecipes(body, homeTab == 0);
        }

        // Chọn 1 trong 5 người đi lại trên map. Không tốn lượt.
        void DrawLeaderPick(Rect r)
        {
            GUI.Label(new Rect(r.x, r.y, r.width, 20), "Người đi lại trong làng hôm nay. Đổi lại được ở Nhà, không tốn lượt.", dim);
            int n = config.friends.Count;
            float cw = (r.width - (n - 1) * 10) / n;
            for (int i = 0; i < n; i++)
            {
                string f = config.friends[i];
                var c = new Rect(r.x + i * (cw + 10), r.y + 30, cw, 196);
                bool on = f == leader;
                Square(c, on ? new Color(1f, 0.85f, 0.3f, 0.18f) : new Color(1f, 1f, 1f, 0.05f));
                if (on) Outline(c, Gold, 2f);
                var face = Tex("Portraits/" + BattleController.SpriteKey(f));
                if (face != null) GUI.DrawTexture(new Rect(c.center.x - 48, c.y + 10, 96, 96), face, ScaleMode.ScaleToFit);
                var walk = Tex("Walk/" + BattleController.SpriteKey(f) + "_down_" + (on ? (int)(Time.time * 4f) % 3 : 0));
                if (walk != null) GUI.DrawTexture(new Rect(c.center.x - 16, c.y + 108, 32, 48), walk);
                var size = header.CalcSize(new GUIContent(f));
                GUI.Label(new Rect(c.center.x - size.x / 2f, c.y + 164, size.x, 24), f, header);
                if (GUI.Button(c, GUIContent.none, GUIStyle.none))
                {
                    leader = f;
                    if (panel == Panel.Leader) Close();
                }
            }
        }

        bool Tab(Rect r, string name, bool on)
        {
            return GUI.Button(r, name, on ? tabOn : btn);
        }

        bool Btn(Rect r, string name)
        {
            return GUI.Button(r, name, btn);
        }

        static void ShadowLabel(Rect r, string s, GUIStyle st)
        {
            var old = st.normal.textColor;
            st.normal.textColor = new Color(0f, 0f, 0f, 0.75f);
            GUI.Label(new Rect(r.x + 1, r.y + 1, r.width, r.height), s, st);
            st.normal.textColor = old;
            GUI.Label(r, s, st);
        }

        void DrawField(Rect r)
        {
            GUI.Label(new Rect(r.x, r.y, r.width, 20), "Ruộng mất khi vòng lặp quay lại. Trồng để có nguyên liệu, không cần tối ưu.", dim);
            int n = state.Plots.Count;
            float cw = (r.width - (n - 1) * 10) / n;
            for (int i = 0; i < n; i++)
            {
                var c = new Rect(r.x + i * (cw + 10), r.y + 30, cw, 296);
                Square(c, new Color(0.24f, 0.18f, 0.12f));
                var p = state.Plots[i];
                GUI.Label(new Rect(c.x + 10, c.y + 8, c.width - 20, 22), "Ô " + (i + 1), header);
                if (p.crop < 0)
                {
                    GUI.Label(new Rect(c.x + 10, c.y + 32, c.width - 20, 20), "Trống. Trồng:", small);
                    for (int kk = 0; kk < config.crops.Count; kk++)
                    {
                        var cd = config.crops[kk];
                        GUI.enabled = state.CanAct;
                        if (Btn(new Rect(c.x + 8, c.y + 56 + kk * 44, c.width - 16, 38), cd.name + " · " + cd.days + " ngày"))
                            state.Plant(i, kk);
                        GUI.enabled = true;
                    }
                }
                else
                {
                    var cd = config.crops[p.crop];
                    bool ready = state.IsReady(i);
                    var tex = Tex("World/crop_" + BattleController.SpriteKey(cd.name) + "_2");
                    if (tex != null) GUI.DrawTexture(new Rect(c.center.x - tex.width * 2, c.y + 96, tex.width * 4, tex.height * 4), tex);
                    GUI.Label(new Rect(c.x + 10, c.y + 34, c.width - 20, 24), cd.name, header);
                    float t = 1f - (float)state.DaysLeft(i) / cd.days;
                    Square(new Rect(c.x + 10, c.y + 62, c.width - 20, 10), new Color(0.15f, 0.15f, 0.15f));
                    Square(new Rect(c.x + 10, c.y + 62, (c.width - 20) * t, 10), ready ? Gold : new Color(0.4f, 0.75f, 0.35f));
                    GUI.Label(new Rect(c.x + 10, c.y + 168, c.width - 20, 60),
                        ready ? "Chín. Thu được " + cd.yieldCount + " " + cd.yield + "." : "Còn " + state.DaysLeft(i) + " ngày", small);
                    GUI.enabled = ready && state.CanAct;
                    if (Btn(new Rect(c.x + 8, c.y + 248, c.width - 16, 40), "Thu hoạch")) state.Harvest(i);
                    GUI.enabled = true;
                }
            }
        }

        void DrawRecipes(Rect r, bool cook)
        {
            GUI.Label(new Rect(r.x, r.y, r.width, 20), cook
                ? "Ăn ngay trong ngày, buff cho đêm nay. Nhiều món không cộng dồn."
                : "Đồ cúng để sửa đình. Bùa và thuốc mang vào trận.", dim);
            float y = r.y + 28;
            foreach (var rc in config.recipes)
            {
                if ((rc.kind == RecipeKind.Food) != cook) continue;
                var row = new Rect(r.x, y, r.width, 54);
                Square(row, new Color(1f, 1f, 1f, 0.04f));
                var ic = Icon(rc.output);
                if (ic != null) GUI.DrawTexture(new Rect(row.x + 6, row.y + 3, 48, 48), ic, ScaleMode.ScaleToFit);
                bool unlocked = state.Unlocked(rc);
                GUI.Label(new Rect(row.x + 64, row.y + 4, 300, 24), rc.output + (cook ? "" : "  (có " + state.Count(rc.output) + ")"),
                    unlocked ? header : dim);
                GUI.Label(new Rect(row.x + 64, row.y + 28, row.width - 200, 22),
                    unlocked ? "Cần: " + NeedsText(rc.needs) + (cook ? " · +" + rc.foodBonusHp + " HP tối đa đêm nay" : "")
                             : "Khóa: cần " + rc.npc + " thân thiết mức " + rc.npcLevel, small);
                GUI.enabled = state.WhyCannotMake(rc) == null;
                if (Btn(new Rect(row.xMax - 120, row.y + 9, 110, 36), cook ? "Nấu" : "Làm")) state.Make(rc);
                GUI.enabled = true;
                y += 60;
            }
        }

        string NeedsText(string[] needs)
        {
            var count = new Dictionary<string, int>();
            var order = new List<string>();
            foreach (var x in needs)
            {
                if (!count.ContainsKey(x)) { count[x] = 0; order.Add(x); }
                count[x]++;
            }
            var parts = new List<string>();
            foreach (var x in order) parts.Add(count[x] + " " + x + " (" + state.Count(x) + ")");
            return string.Join(", ", parts.ToArray());
        }

        void DrawNpc(Rect r, NpcDef npc)
        {
            if (npc == null)
            {
                GUI.Label(new Rect(r.x, r.y, r.width, 24), "Không có NPC \"" + openSpot.npc + "\" trong Village Config.", dim);
                return;
            }
            int lv = state.Affinity[npc.name];
            GUI.Label(new Rect(r.x, r.y, r.width - 140, 20), npc.role, small);
            GUI.Label(new Rect(r.x, r.y + 26, 120, 22), "Thân thiết", text);
            for (int i = 0; i < config.maxAffinity; i++)
                Square(new Rect(r.x + 100 + i * 20, r.y + 31, 14, 14), i < lv ? Gold : Off);
            GUI.enabled = state.CanAct && lv < config.maxAffinity;
            if (Btn(new Rect(r.xMax - 130, r.y + 6, 130, 40), "Thăm")) state.Visit(npc);
            GUI.enabled = true;

            float y = r.y + 62;
            for (int i = 0; i < config.maxAffinity && i < npc.levelNotes.Length; i++)
            {
                var st = i < lv ? gold : (i == lv ? small : dim);
                string mark = i < lv ? "Đã mở" : (i == lv ? "Lần thăm tới" : "");
                GUI.Label(new Rect(r.x, y, 110, 22), "Mức " + (i + 1), st);
                GUI.Label(new Rect(r.x + 70, y, r.width - 200, 22), npc.levelNotes[i], st);
                GUI.Label(new Rect(r.xMax - 120, y, 120, 22), mark, st);
                y += 26;
            }
        }

        void DrawDinh(Rect r)
        {
            GUI.Label(new Rect(r.x, r.y, r.width, 40),
                "Dâng 1 bộ lễ để khôi phục một nghi lễ. Mỗi nghi lễ mở thêm chỗ để đi đêm. Đình không mất khi vòng lặp quay lại.", small);
            float x = r.x;
            foreach (var item in config.ritualSet)
            {
                var c = new Rect(x, r.y + 50, 140, 150);
                Square(c, new Color(1f, 1f, 1f, 0.04f));
                var ic = Icon(item);
                if (ic != null) GUI.DrawTexture(new Rect(c.x + 38, c.y + 10, 64, 64), ic, ScaleMode.ScaleToFit);
                GUI.Label(new Rect(c.x + 6, c.y + 82, c.width - 12, 40), item, small);
                int have = state.Count(item);
                GUI.Label(new Rect(c.x + 6, c.y + 120, c.width - 12, 24), "Có " + have, have > 0 ? gold : dim);
                x += 150;
            }
            GUI.Label(new Rect(r.x, r.y + 214, r.width, 24),
                "Nghi lễ đã khôi phục: " + state.Rituals + " · Trận mở: " + state.UnlockedShrines + "/" + NightNames.Length, header);
            string why = state.WhyCannotRepair();
            GUI.enabled = why == null;
            if (Btn(new Rect(r.x, r.y + 250, 220, 42), "Dâng lễ sửa đình")) state.RepairDinh();
            GUI.enabled = true;
            if (why != null) GUI.Label(new Rect(r.x + 232, r.y + 260, r.width - 240, 24), why, dim);
        }

        // Nói chuyện với 1 người bạn đứng trong làng: rủ đi tìm manh mối (1 lượt).
        void DrawClue(Rect r)
        {
            string f = clueFriend;
            var face = Tex("Portraits/" + BattleController.SpriteKey(f));
            if (face != null) GUI.DrawTexture(new Rect(r.x, r.y, 120, 120), face, ScaleMode.ScaleToFit);
            float tx = r.x + 136;
            int b = state.Bond.ContainsKey(f) ? state.Bond[f] : 0;
            GUI.Label(new Rect(tx, r.y, 200, 22), "Gắn kết", text);
            for (int i = 0; i < config.maxBond; i++)
                Square(new Rect(tx + 80 + i * 20, r.y + 5, 14, 14), i < b ? new Color(0.55f, 0.8f, 1f) : Off);
            GUI.Label(new Rect(tx, r.y + 30, r.width - 136, 40),
                "Đi cùng " + f + " tìm manh mối: mở 1 mảnh ký ức, +1 gắn kết. Ký ức đã mở: " + state.Memories + "/" + config.memoryCount + ".", small);
            GUI.Label(new Rect(tx, r.y + 72, r.width - 136, 22), "Nội dung từng mảnh ký ức sẽ viết sau; bản này chỉ đếm tiến độ.", dim);
            GUI.enabled = state.CanAct && state.Bond.ContainsKey(f);
            if (Btn(new Rect(tx, r.y + 112, 300, 42), "Đi tìm manh mối cùng " + f + " (1 lượt)"))
            {
                state.SeekClue(f);
                Close();
            }
            GUI.enabled = true;
        }

        void DrawNightPick(Rect r)
        {
            GUI.Label(new Rect(r.x, r.y, r.width, 20), state.CanAct
                ? "Còn " + state.ActionsLeft + " lượt chưa dùng sẽ bị bỏ. Bùa và thuốc trong túi mang theo."
                : "Bùa và thuốc trong túi mang theo.", dim);
            for (int i = 0; i < NightNames.Length; i++)
            {
                bool open = i < state.UnlockedShrines;
                GUI.enabled = open;
                if (Btn(new Rect(r.x, r.y + 30 + i * 56, 380, 46), NightNames[i])) GoNight(i);
                GUI.enabled = true;
                if (!open) GUI.Label(new Rect(r.x + 392, r.y + 42 + i * 56, 220, 24), "Sửa đình để mở", dim);
            }
        }

        // ---------- tiện ích ----------

        Texture2D Tex(string path)
        {
            Texture2D t;
            if (!texCache.TryGetValue(path, out t))
            {
                t = PixelTex.Load(path);
                texCache[path] = t;
            }
            return t;
        }

        Texture2D Icon(string name)
        {
            return Tex("Items/" + BattleController.SpriteKey(name));
        }

        void EnsureStyles()
        {
            if (title != null) return;
            title = new GUIStyle(GUI.skin.label) { fontSize = 20, fontStyle = FontStyle.Bold };
            header = new GUIStyle(GUI.skin.label) { fontSize = 16, fontStyle = FontStyle.Bold };
            text = new GUIStyle(GUI.skin.label) { fontSize = 15 };
            small = new GUIStyle(GUI.skin.label) { fontSize = 13, wordWrap = true };
            dim = new GUIStyle(GUI.skin.label) { fontSize = 13, wordWrap = true };
            dim.normal.textColor = new Color(0.6f, 0.6f, 0.66f);
            right = new GUIStyle(GUI.skin.label) { fontSize = 15, alignment = TextAnchor.UpperRight };
            gold = new GUIStyle(GUI.skin.label) { fontSize = 13, wordWrap = true };
            gold.normal.textColor = Gold;
            label = new GUIStyle(GUI.skin.label) { fontSize = 14, fontStyle = FontStyle.Bold, wordWrap = false };
            label.normal.textColor = Cream;
            tip = new GUIStyle(GUI.skin.label) { fontSize = 13, wordWrap = true };
            tip.normal.textColor = new Color(0.22f, 0.15f, 0.1f);
            title.normal.textColor = Cream;
            header.normal.textColor = Cream;
            text.normal.textColor = Cream;
            small.normal.textColor = new Color(0.86f, 0.82f, 0.72f);
            right.normal.textColor = Cream;
            UiSkin.Build(Tex, out panelSt, out btn, out tabOn, out plaqueSt, out tipSt);
        }

        static void Square(Rect r, Color c)
        {
            var old = GUI.color;
            GUI.color = c;
            GUI.DrawTexture(r, Texture2D.whiteTexture);
            GUI.color = old;
        }

        void Box(Rect r)
        {
            if (panelSt != null) GUI.Box(r, GUIContent.none, panelSt);
            else Square(r, new Color(0.1f, 0.09f, 0.12f, 0.96f));
        }

        static void Outline(Rect r, Color c, float t)
        {
            Square(new Rect(r.x, r.y, r.width, t), c);
            Square(new Rect(r.x, r.yMax - t, r.width, t), c);
            Square(new Rect(r.x, r.y, t, r.height), c);
            Square(new Rect(r.xMax - t, r.y, t, r.height), c);
        }
    }
}
