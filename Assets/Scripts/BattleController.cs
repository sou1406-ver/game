using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    // Sprint 0 — Combat lõi, lượt theo Tốc độ.
    // Gắn vào một GameObject rỗng trong scene trống rồi bấm Play. Không cần prefab, sprite hay Canvas.
    public class BattleController : MonoBehaviour
    {
        enum Phase { PlayerTurn, Busy, Timing, Parry, Victory, Defeat }
        enum Pending { None, Attack, Skill, Ulti, Item }

        [Header("Để trống = dùng số mặc định")]
        [SerializeField] BalanceConfig balance;
        [SerializeField] CharacterData[] party = new CharacterData[3];
        [SerializeField] EnemyData[] enemies = new EnemyData[2];   // trận 1
        [SerializeField] EnemyData[] enemies2 = new EnemyData[2];  // trận 2 (phím T để đổi)
        [SerializeField] ItemData[] items = new ItemData[3];

        BattleContext ctx;
        Phase phase;
        Pending pending;
        int round;
        string message = "";

        // Thứ tự lượt trong vòng
        readonly List<Combatant> turnQueue = new List<Combatant>();
        int turnIndex;
        Combatant current;

        // Tuyệt kỹ
        float timingCursor, timingZone;
        Combatant ultiTarget;
        int ultiHit;

        // Gạt đòn
        float parryCursor, parryZone;
        bool parrySuccess;
        string parryLabel = "";

        // Menu lệnh và chọn mục tiêu
        int menuIndex, targetIndex;
        int encounter; // 0 = trận 1, 1 = trận 2

        // Túi đồ chung của đội: bag[i] = số món items[i] còn lại trong trận
        int[] bag = new int[0];
        bool itemMenu;
        int itemIndex, selectedItem;

        GUIStyle nameStyle, textStyle, smallStyle, rightSmallStyle, intentStyle, bigStyle, hintStyle,
            menuStyle, menuDisabledStyle, descStyle, statusStyle, centerStyle, markerStyle;

        // ---------- Dữ liệu mặc định ----------

        void EnsureDefaults()
        {
            if (balance == null) balance = BalanceConfig.CreateDefault();

            if (party == null || party.Length == 0) party = new CharacterData[3];
            //                                   tên     màu                              HP Công Thủ Crit Tốc Né Luck kháng
            if (party.Length > 0 && party[0] == null)
                party[0] = CharacterData.Create("Vy", new Color(0.95f, 0.45f, 0.45f), 22, 4, 2, 10, 12, 10, 3, 0.05f,
                    "Phá đòn", SkillType.CancelIntent, 0f, "Kiểm soát · Phá đòn");
            if (party.Length > 1 && party[1] == null) // luật đọc văn tự chưa có trong GDD: tạm vẫn là đòn mạnh x2
                party[1] = CharacterData.Create("Tuấn", new Color(0.85f, 0.2f, 0.2f), 26, 7, 2, 15, 9, 5, 2, 0f,
                    "Đọc văn tự", SkillType.PowerStrike, 2f, "Sát thương · Đọc văn tự");
            if (party.Length > 2 && party[2] == null)
                party[2] = CharacterData.Create("Khoa", new Color(0.65f, 0.15f, 0.15f), 32, 4, 5, 5, 6, 0, 1, 0.25f,
                    "Che chắn", SkillType.Shield, 8f, "Đỡ đòn · Kháng Âm khí");

            // Hình nhân vật: Assets/Resources/Characters/<tên>.png
            foreach (var d in party)
                if (d != null && d.sprite == null) d.sprite = PixelTex.Load("Characters/" + SpriteKey(d.displayName));

            if (enemies == null || enemies.Length == 0) enemies = new EnemyData[2];
            //                                   tên       màu                             HP Thủ Crit Tốc Né
            if (enemies.Length > 0 && enemies[0] == null)
                enemies[0] = EnemyData.Create("Ma đói", new Color(0.3f, 0.45f, 0.95f), 30, 1, 10, 10, 5,
                    new IntentDef("Cắn", IntentType.SingleHit, 7, TargetRule.LowestHP),
                    new IntentDef("Cào", IntentType.SingleHit, 5, TargetRule.HighestAmKhi),
                    new IntentDef("Rít", IntentType.Terrify, 8, TargetRule.All));
            if (enemies.Length > 1 && enemies[1] == null)
                enemies[1] = EnemyData.Create("Ma nước", new Color(0.35f, 0.75f, 0.95f), 24, 0, 0, 7, 10,
                    new IntentDef("Sóng lạnh", IntentType.AllHit, 3, TargetRule.All),
                    new IntentDef("Kéo", IntentType.SingleHit, 6, TargetRule.HighestAmKhi));

            if (items == null || items.Length == 0) items = new ItemData[3];
            //                                                                  sức  số lượng
            if (items.Length > 0 && items[0] == null) items[0] = ItemData.Create("Bùa vàng", ItemEffect.Talisman, 8, 2);
            if (items.Length > 1 && items[1] == null) items[1] = ItemData.Create("Thuốc hồi HP", ItemEffect.HealHP, 10, 2);
            if (items.Length > 2 && items[2] == null) items[2] = ItemData.Create("Thuốc giảm Âm khí", ItemEffect.CleanseAmKhi, 30, 1);
            // Icon đồ: Assets/Resources/Items/<tên>.png (Bùa vàng → bua_vang)
            foreach (var d in items)
                if (d != null && d.icon == null) d.icon = PixelTex.Load("Items/" + SpriteKey(d.displayName));

            if (enemies2 == null || enemies2.Length == 0) enemies2 = new EnemyData[2];
            //                                    tên       màu                              HP Thủ Crit Tốc Né
            if (enemies2.Length > 0 && enemies2[0] == null)
                enemies2[0] = EnemyData.Create("Ma nhện", new Color(0.45f, 0.35f, 0.55f), 26, 2, 5, 13, 10,
                    new IntentDef("Cắn độc", IntentType.SingleHit, 6, TargetRule.LowestHP),
                    new IntentDef("Thì thầm", IntentType.Terrify, 10, TargetRule.All),
                    new IntentDef("Quăng tơ", IntentType.AllHit, 4, TargetRule.All));
            if (enemies2.Length > 1 && enemies2[1] == null)
                enemies2[1] = EnemyData.Create("Ma đói", new Color(0.3f, 0.45f, 0.95f), 30, 1, 10, 10, 5,
                    new IntentDef("Cắn", IntentType.SingleHit, 7, TargetRule.LowestHP),
                    new IntentDef("Cào", IntentType.SingleHit, 5, TargetRule.HighestAmKhi),
                    new IntentDef("Rít", IntentType.Terrify, 8, TargetRule.All));

            // Chân dung: Assets/Resources/Portraits/<tên>.png
            foreach (var d in party)
                if (d != null && d.portrait == null) d.portrait = PixelTex.Load("Portraits/" + SpriteKey(d.displayName));

            // Hình quái: Assets/Resources/Enemies/<tên>.png (Ma đói → ma_doi)
            foreach (var d in enemies2)
                if (d != null && d.sprite == null) d.sprite = PixelTex.Load("Enemies/" + SpriteKey(d.displayName));
            foreach (var d in enemies)
                if (d != null && d.sprite == null) d.sprite = PixelTex.Load("Enemies/" + SpriteKey(d.displayName));
        }

        // Bỏ dấu tiếng Việt, khoảng trắng thành "_": "Ma đói" → "ma_doi", "Tuấn" → "tuan".
        public static string SpriteKey(string name)
        {
            var sb = new System.Text.StringBuilder();
            foreach (char ch in name.ToLowerInvariant().Normalize(System.Text.NormalizationForm.FormD))
            {
                var cat = System.Globalization.CharUnicodeInfo.GetUnicodeCategory(ch);
                if (cat == System.Globalization.UnicodeCategory.NonSpacingMark) continue;
                if (ch == 'đ') sb.Append('d');
                else if (ch == ' ') sb.Append('_');
                else sb.Append(ch);
            }
            return sb.ToString();
        }

        // ---------- Vòng và lượt ----------

        // Chạy riêng (autoStart) thì tự vào trận. Có DayController thì làng gọi StartBattle mỗi đêm.
        [HideInInspector] public bool autoStart = true;

        // Gọi khi bấm "Về làng": (thắng?, số đồ còn lại theo tên)
        public System.Action<bool, Dictionary<string, int>> OnFinished;

        Dictionary<string, int> presetBag; // túi đồ mang từ làng vào
        int bonusMaxHp;                    // buff món ăn trong ngày

        bool DayMode
        {
            get { return OnFinished != null; }
        }

        void Start()
        {
            EnsureDefaults();
            if (autoStart) BuildBattle();
        }

        public void StartBattle(Dictionary<string, int> bagByName, int encounterIndex, int bonusHp)
        {
            EnsureDefaults();
            presetBag = bagByName;
            encounter = Mathf.Clamp(encounterIndex, 0, 1);
            bonusMaxHp = bonusHp;
            BuildBattle();
        }

        // Ẩn trận (OnGUI không vẽ gì khi ctx == null).
        public void Hide()
        {
            StopAllCoroutines();
            ctx = null;
        }

        Dictionary<string, int> BagByName()
        {
            var d = new Dictionary<string, int>();
            for (int i = 0; i < items.Length; i++) d[items[i].displayName] = bag[i];
            return d;
        }

        void SwitchEncounter()
        {
            encounter = 1 - encounter;
            BuildBattle();
        }

        void BuildBattle()
        {
            StopAllCoroutines();
            ctx = new BattleContext { Cfg = balance };
            foreach (var d in party) if (d != null) ctx.Allies.Add(Combatant.FromCharacter(d, balance));
            foreach (var a in ctx.Allies)
            {
                a.MaxHP += bonusMaxHp;
                a.HP += bonusMaxHp;
            }
            foreach (var d in encounter == 0 ? enemies : enemies2) if (d != null) ctx.Enemies.Add(Combatant.FromEnemy(d, balance));
            round = 0;
            message = "";
            current = null;
            items = System.Array.FindAll(items, d => d != null);
            bag = new int[items.Length];
            for (int i = 0; i < items.Length; i++)
            {
                int n;
                bag[i] = presetBag == null ? items[i].startCount
                    : presetBag.TryGetValue(items[i].displayName, out n) ? n : 0;
            }
            itemMenu = false;
            anims.Clear();
            popups.Clear();
            startT = Time.time;
            flashText = "";
            BeginRound();
        }

        void BeginRound()
        {
            round++;
            ctx.Log.Add("— Vòng " + round + " —");

            foreach (var a in ctx.Allies)
            {
                if (!a.PossessedPending || !a.IsAlive) continue;
                a.PossessedPending = false;
                a.Possessed = true;
                a.PossessionTarget = LowestHpOther(a);
                ctx.Log.Add(a.Name + " bị nhập!");
            }

            foreach (var e in ctx.Enemies) EnemyBrain.PlanIntent(e, ctx.Allies);

            // Ai nhanh đi trước; bằng Tốc độ thì người chơi đi trước.
            turnQueue.Clear();
            turnQueue.AddRange(ctx.Allies.FindAll(c => c.IsAlive));
            turnQueue.AddRange(ctx.Enemies.FindAll(c => c.IsAlive));
            var order = new List<Combatant>(turnQueue);
            turnQueue.Sort((x, y) =>
            {
                if (x.Speed != y.Speed) return y.Speed.CompareTo(x.Speed);
                if (x.IsAlly != y.IsAlly) return x.IsAlly ? -1 : 1;
                return order.IndexOf(x).CompareTo(order.IndexOf(y));
            });
            turnIndex = 0;
            NextTurn();
        }

        void NextTurn()
        {
            if (CheckEnd()) return;

            while (turnIndex < turnQueue.Count && !turnQueue[turnIndex].IsAlive) turnIndex++;
            if (turnIndex >= turnQueue.Count)
            {
                BeginRound();
                return;
            }

            current = turnQueue[turnIndex];
            turnIndex++;

            if (!current.IsAlly)
            {
                StartCoroutine(EnemyTurn(current));
                return;
            }

            current.Guarding = false; // Đỡ hết hiệu lực khi đến lượt mình
            if (current.Possessed)
            {
                StartCoroutine(PossessedTurn(current));
                return;
            }

            phase = Phase.PlayerTurn;
            pending = Pending.None;
            itemMenu = false;
            menuIndex = 0;
        }

        void EndAllyTurn()
        {
            pending = Pending.None;
            itemMenu = false;
            if (CheckEnd()) return;
            StartCoroutine(AfterAllyTurn());
        }

        IEnumerator AfterAllyTurn()
        {
            phase = Phase.Busy;
            yield return new WaitForSeconds(balance.turnDelay);
            NextTurn();
        }

        IEnumerator EnemyTurn(Combatant e)
        {
            phase = Phase.Busy;
            yield return new WaitForSeconds(balance.enemyActionDelay);

            bool parried = false;
            if (e.Intent != null && !e.IntentCanceled && EnemyBrain.IsAttack(e.Intent))
            {
                parryLabel = e.Name + " (" + e.Intent.label + ")";
                parryCursor = 0f;
                parryZone = Random.Range(balance.parryZoneMin, balance.parryZoneMax);
                parrySuccess = false;
                phase = Phase.Parry;
                while (phase == Phase.Parry) yield return null;
                parried = parrySuccess;
            }

            if (e.Intent != null && !e.IntentCanceled) Act(e);
            EnemyBrain.Execute(e, ctx, parried);
            yield return new WaitForSeconds(balance.turnDelay);
            NextTurn();
        }

        IEnumerator PossessedTurn(Combatant a)
        {
            phase = Phase.Busy;
            yield return new WaitForSeconds(balance.enemyActionDelay);
            if (a.PossessionTarget != null && a.PossessionTarget.IsAlive)
            {
                Act(a);
                CombatRules.Hit(a.PossessionTarget, a.Attack, true, false, a.Name + " (bị nhập)", balance, ctx.Log);
            }
            a.Possessed = false;
            a.PossessionTarget = null;
            if (a.IsAlive)
            {
                a.AmKhi = balance.amKhiAfterPossession;
                ctx.Log.Add(a.Name + " tỉnh lại.");
            }
            yield return new WaitForSeconds(balance.turnDelay);
            NextTurn();
        }

        bool CheckEnd()
        {
            if (ctx.Enemies.TrueForAll(e => !e.IsAlive)) { phase = Phase.Victory; return true; }
            if (ctx.Allies.TrueForAll(a => !a.IsAlive)) { phase = Phase.Defeat; return true; }
            return false;
        }

        Combatant LowestHpOther(Combatant self)
        {
            Combatant best = null;
            foreach (var a in ctx.Allies)
                if (a != self && a.IsAlive && (best == null || a.HP < best.HP)) best = a;
            return best;
        }

        // ---------- Lệnh của người chơi ----------

        bool MyTurn
        {
            get { return phase == Phase.PlayerTurn && current != null && current.IsAlly; }
        }

        void Issue(ICommand cmd)
        {
            string reason;
            if (!cmd.CanExecute(ctx, out reason))
            {
                message = reason;
                return;
            }
            if (!(cmd is GuardCommand)) Act(current);
            cmd.Execute(ctx);
            message = "";
            EndAllyTurn();
        }

        void OnAllyClicked(Combatant a)
        {
            if (!MyTurn) return;
            if (pending == Pending.Skill && current.CharData.SkillTargetsAlly) Issue(new SkillCommand(current, a));
            else if (pending == Pending.Item && items[selectedItem].TargetsAlly) Issue(UseItem(a));
        }

        void OnEnemyClicked(Combatant e)
        {
            if (!MyTurn) return;
            if (pending == Pending.Attack) Issue(new AttackCommand(current, e));
            else if (pending == Pending.Skill && !current.CharData.SkillTargetsAlly) Issue(new SkillCommand(current, e));
            else if (pending == Pending.Ulti) BeginUlti(e);
            else if (pending == Pending.Item && !items[selectedItem].TargetsAlly) Issue(UseItem(e));
        }

        ItemCommand UseItem(Combatant target)
        {
            return new ItemCommand(current, items[selectedItem], bag, selectedItem, target);
        }

        // ---------- Tuyệt kỹ: mỗi đòn đi qua thanh căng nhịp ----------

        void BeginUlti(Combatant target)
        {
            var cmd = new UltiCommand(current, target);
            string reason;
            if (!cmd.CanExecute(ctx, out reason))
            {
                message = reason;
                return;
            }
            cmd.Execute(ctx);
            pending = Pending.None;
            ultiTarget = target;
            ultiHit = 1;
            message = "";
            StartTimingBar();
        }

        void StartTimingBar()
        {
            timingCursor = 0f;
            timingZone = Random.Range(balance.timingZoneMin, balance.timingZoneMax);
            phase = Phase.Timing;
        }

        void ResolveTiming()
        {
            if (phase != Phase.Timing || ultiTarget == null) return;

            int bonus = CombatRules.TimingBonus(timingCursor, timingZone, balance);
            Act(current);
            CombatRules.UltiHit(current, ultiTarget, ultiHit, bonus, balance, ctx.Log);
            message = "";
            if (bonus >= balance.timingMaxBonus * 0.75f) Flash("CHUẨN! +" + bonus + "% crit", Gold);
            else if (bonus > 0) Flash("+" + bonus + "% crit", new Color(1f, 0.95f, 0.75f));
            else Flash("Trượt nhịp", new Color(0.7f, 0.7f, 0.75f));

            ultiHit++;
            if (ultiHit <= balance.ultiHits && ultiTarget.IsAlive)
            {
                StartTimingBar();
                return;
            }

            ultiTarget = null;
            EndAllyTurn();
        }

        // pressed = người chơi bấm; hết thời gian mà không bấm thì thất bại.
        void ResolveParry(bool pressed)
        {
            if (phase != Phase.Parry) return;
            parrySuccess = pressed && Mathf.Abs(parryCursor - parryZone) <= balance.parryZoneWidth * 0.5f;
            message = "";
            if (parrySuccess) Flash("GẠT!", Gold);
            else Flash(pressed ? "Hụt nhịp" : "Không kịp", new Color(1f, 0.55f, 0.5f));
            phase = Phase.Busy;
        }

        void Update()
        {
            if (ctx == null) return;
            if (phase == Phase.Parry)
            {
                parryCursor += Time.deltaTime / Mathf.Max(0.1f, balance.parryDuration);
                if (parryCursor >= 1f)
                {
                    parryCursor = 1f;
                    ResolveParry(false);
                }
            }
            else if (phase == Phase.Timing)
            {
                timingCursor += Time.deltaTime / Mathf.Max(0.1f, balance.timingDuration);
                if (timingCursor >= 1f)
                {
                    timingCursor = 1f;
                    ResolveTiming();
                }
            }
        }

        // ---------- Menu lệnh và chọn mục tiêu ----------

        static readonly string[] MenuBase = { "Đánh", "Đỡ", "Skill", "Tuyệt kỹ", "Đồ", "Chờ" };
        static readonly Color Gold = new Color(1f, 0.85f, 0.3f);
        static readonly Color Cream = new Color(0.93f, 0.89f, 0.77f);
        static readonly Color HpColor = new Color(0.86f, 0.24f, 0.22f);
        static readonly Color AmKhiColor = new Color(0.62f, 0.36f, 0.82f);
        static readonly Color ManaColor = new Color(0.32f, 0.58f, 0.96f);
        static readonly Color RageColor = new Color(0.95f, 0.55f, 0.15f);

        string MenuLabel(int i)
        {
            if (i == 2) return current.CharData.skillName;
            if (i == 3) return current.CharData.ultiName;
            return MenuBase[i];
        }

        string MenuCost(int i)
        {
            if (i == 2) return balance.skillManaCost + " MP";
            if (i == 3) return current.Rage >= balance.rageMax ? "Nộ đầy" : current.Rage + "/" + balance.rageMax;
            if (i == 4)
            {
                int n = 0;
                foreach (var c in bag) n += c;
                return "x" + n;
            }
            return "";
        }

        bool MenuEnabled(int i)
        {
            if (i == 2) return current.Mana >= balance.skillManaCost;
            if (i == 3) return current.Rage >= balance.rageMax;
            if (i == 4) return HasAnyItem;
            return true;
        }

        string MenuDescription(int i)
        {
            switch (i)
            {
                case 0: return "Đánh 1 quái. Hồi " + balance.manaPerAttack + " MP, +" + balance.ragePerAttack + " Nộ.";
                case 1: return "Đòn kế tiếp giảm " + Mathf.RoundToInt(balance.guardReduction * 100) + "%, hết khi đến lượt sau.";
                case 2: return SkillDescription(current.CharData) + (MenuEnabled(2) ? "" : " Không đủ MP.");
                case 3: return balance.ultiHits + " đòn liền, mỗi đòn bấm nhịp để tăng crit." + (MenuEnabled(3) ? "" : " Nộ chưa đầy.");
                case 4: return HasAnyItem ? "Dùng đồ trong túi chung. Tốn lượt." : "Túi đồ đã hết.";
                default: return "Bỏ lượt.";
            }
        }

        static string SkillDescription(CharacterData d)
        {
            switch (d.skillType)
            {
                case SkillType.CancelIntent: return "Hủy ý định đã báo của 1 quái.";
                case SkillType.Shield: return "Khiên " + Mathf.RoundToInt(d.skillPower) + " cho 1 đồng đội.";
                default: return "Đòn mạnh x" + d.skillPower + " vào 1 quái.";
            }
        }

        void Choose(int i)
        {
            if (!MyTurn || !MenuEnabled(i)) return;
            message = "";
            switch (i)
            {
                case 0: StartTargeting(Pending.Attack); break;
                case 1: Issue(new GuardCommand(current)); break;
                case 2: StartTargeting(Pending.Skill); break;
                case 3: StartTargeting(Pending.Ulti); break;
                case 4:
                    itemMenu = true;
                    itemIndex = System.Array.FindIndex(bag, c => c > 0);
                    break;
                default:
                    ctx.Log.Add(current.Name + " chờ.");
                    EndAllyTurn();
                    break;
            }
        }

        bool HasAnyItem
        {
            get { return System.Array.Exists(bag, c => c > 0); }
        }

        void ChooseItem(int i)
        {
            if (!MyTurn || i < 0 || i >= items.Length || bag[i] <= 0) return;
            message = "";
            selectedItem = i;
            StartTargeting(Pending.Item);
        }

        bool TargetsAllies
        {
            get
            {
                if (current == null) return false;
                if (pending == Pending.Skill) return current.CharData.SkillTargetsAlly;
                if (pending == Pending.Item) return items[selectedItem].TargetsAlly;
                return false;
            }
        }

        List<Combatant> Targets()
        {
            var list = TargetsAllies ? ctx.Allies : ctx.Enemies;
            return list.FindAll(c => c.IsAlive);
        }

        void StartTargeting(Pending p)
        {
            pending = p;
            targetIndex = 0;
            if (!TargetsAllies) return;
            var t = Targets();
            bool byAmKhi = p == Pending.Item && items[selectedItem].effect == ItemEffect.CleanseAmKhi;
            for (int k = 1; k < t.Count; k++) // mặc định: Âm khí cao nhất (thuốc giảm Âm khí), còn lại máu thấp nhất
                if (byAmKhi ? t[k].AmKhi > t[targetIndex].AmKhi : t[k].HP < t[targetIndex].HP) targetIndex = k;
        }

        Combatant TargetedNow()
        {
            if (!MyTurn || pending == Pending.None) return null;
            var t = Targets();
            if (t.Count == 0) return null;
            targetIndex = Mathf.Clamp(targetIndex, 0, t.Count - 1);
            return t[targetIndex];
        }

        void ConfirmTarget(Combatant c)
        {
            if (c.IsAlly) OnAllyClicked(c);
            else OnEnemyClicked(c);
        }

        void HandleKeys()
        {
            var ev = Event.current;
            if (ev.type != EventType.KeyDown) return;
            var k = ev.keyCode;
            bool confirm = k == KeyCode.Space || k == KeyCode.Return || k == KeyCode.KeypadEnter;

            if (k == KeyCode.R && !DayMode) { BuildBattle(); ev.Use(); return; }
            if (k == KeyCode.T && !DayMode) { SwitchEncounter(); ev.Use(); return; }
            if (phase == Phase.Parry) { if (confirm) { ResolveParry(true); ev.Use(); } return; }
            if (phase == Phase.Timing) { if (confirm) { ResolveTiming(); ev.Use(); } return; }
            if (!MyTurn) return;

            bool up = k == KeyCode.UpArrow || k == KeyCode.W;
            bool down = k == KeyCode.DownArrow || k == KeyCode.S;
            bool left = k == KeyCode.LeftArrow || k == KeyCode.A;
            bool right = k == KeyCode.RightArrow || k == KeyCode.D;
            int n = MenuBase.Length;

            if (pending == Pending.None && itemMenu)
            {
                int m = items.Length;
                if (k == KeyCode.Escape) { itemMenu = false; message = ""; }
                else if (up && m > 0) itemIndex = (itemIndex + m - 1) % m;
                else if (down && m > 0) itemIndex = (itemIndex + 1) % m;
                else if (confirm) ChooseItem(itemIndex);
                else return;
            }
            else if (pending == Pending.None)
            {
                if (up) menuIndex = (menuIndex + n - 1) % n;
                else if (down) menuIndex = (menuIndex + 1) % n;
                else if (confirm) Choose(menuIndex);
                else return;
            }
            else
            {
                var t = Targets();
                if (k == KeyCode.Escape) { pending = Pending.None; message = ""; }
                else if ((left || up) && t.Count > 0) targetIndex = (targetIndex + t.Count - 1) % t.Count;
                else if ((right || down) && t.Count > 0) targetIndex = (targetIndex + 1) % t.Count;
                else if (confirm && t.Count > 0) ConfirmTarget(t[Mathf.Clamp(targetIndex, 0, t.Count - 1)]);
                else return;
            }
            ev.Use();
        }

        // ---------- Bố cục nhìn ngang ----------
        // Sân trận vẽ bằng pixel màn hình với tỉ lệ nguyên (px), cao khoảng 270 pixel trận; giao diện vẽ bằng toạ độ ảo cao 720.

        const float BackdropGround = 118f; // dòng bờ đất trong Battle/backdrop.png (draw_battle.py)
        int px = 3;              // pixel màn hình cho 1 pixel trận
        float viewW, viewH;      // khung nhìn, pixel trận
        float guiS = 1f;         // pixel màn hình cho 1 đơn vị ảo
        float startT;            // lúc vào trận, để hiện tiêu đề
        float shakeT = -9f, shakeMag;
        Vector2 camShake;
        string flashText = "";
        Color flashColor;
        float flashT = -9f;
        readonly Dictionary<string, Texture2D> texCache = new Dictionary<string, Texture2D>();
        GUIStyle panelSt, btnSt, tabOnSt, plaqueSt, tipSt;

        bool Ended
        {
            get { return phase == Phase.Victory || phase == Phase.Defeat; }
        }

        float GroundY
        {
            get { return Mathf.Round(viewH * 0.64f); }
        }

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

        // Chỗ đứng (chân) theo thứ tự trong đội: người cuối danh sách đứng sát giữa sân.
        Vector2 SlotPos(Combatant c)
        {
            var list = c.IsAlly ? ctx.Allies : ctx.Enemies;
            int i = list.IndexOf(c), n = list.Count;
            float cx = Mathf.Round(viewW / 2f);
            if (c.IsAlly)
            {
                int back = n - 1 - i;
                return new Vector2(cx - 42 - back * 30, GroundY + (back % 2) * 8);
            }
            return new Vector2(cx + 48 + i * 46, GroundY + (i % 2) * 8);
        }

        Rect ViewToScreen(Rect r)
        {
            return new Rect((Mathf.Round(r.x) + camShake.x) * px, (Mathf.Round(r.y) + camShake.y) * px, r.width * px, r.height * px);
        }

        Rect ToGui(Rect screen)
        {
            return new Rect(screen.x / guiS, screen.y / guiS, screen.width / guiS, screen.height / guiS);
        }

        // Sprite nhìn ngang: đội quay phải (Resources/Walk), quái quay trái (Resources/Battle). Thiếu thì dùng hình cũ.
        Texture2D SpriteFor(Combatant c, out bool fallback)
        {
            fallback = false;
            string key = SpriteKey(c.Name);
            var an = AnimOf(c);
            bool hurt = !c.IsAlive || Time.time - an.hitT < HitTime;
            bool atk = !hurt && Time.time - an.actT < ActTime;
            string idle = (((int)(Time.time * 1.6f)) + (c.IsAlly ? ctx.Allies.IndexOf(c) : ctx.Enemies.IndexOf(c))) % 2 == 0 ? "0" : "1";
            // Sprite trận riêng: Battle/<tên>_0, _1 (thở), _atk, _hurt (extract_ref.py, từ ảnh <tên>_battle.png)
            var b = Tex("Battle/" + key + "_" + (hurt ? "hurt" : atk ? "atk" : idle));
            if (b == null && (hurt || atk)) b = Tex("Battle/" + key + "_0");
            if (b != null) return b;
            if (c.IsAlly)
            {
                var t = Tex("Walk/" + key + "_right_" + (hurt ? "hurt" : atk ? "atk" : "0"));
                if (t != null) return t;
                fallback = true;
                return c.CharData.sprite;
            }
            fallback = true;
            return c.EnemyData.sprite;
        }

        // ---------- UI ----------

        void OnGUI()
        {
            if (ctx == null) return;
            EnsureStyles();
            HandleKeys();
            guiS = Screen.height / 720f;
            px = Mathf.Max(1, Mathf.RoundToInt(Screen.height / 200f)); // sân trận cao ~200 pixel: nhân vật to hơn ngoài làng
            viewW = Screen.width / (float)px;
            viewH = Screen.height / (float)px;

            GUI.matrix = Matrix4x4.identity;
            DrawBattlefield();

            GUI.matrix = Matrix4x4.Scale(new Vector3(guiS, guiS, 1f));
            float w = Screen.width / guiS;
            DrawFieldLabels();
            DrawTopBar(w);
            DrawMessage(w);
            DrawLog();
            DrawCards(w);
            if (MyTurn && pending == Pending.None) DrawCommandMenu();
            else DrawWaitPanel();
            if (phase == Phase.Timing) DrawTimingBar(w, timingCursor, timingZone, balance.timingZoneWidth, Gold, false);
            if (phase == Phase.Parry) DrawTimingBar(w, parryCursor, parryZone, balance.parryZoneWidth, new Color(0.95f, 0.3f, 0.3f), true);
            DrawPopups();
            DrawFlash(w);
            DrawIntro(w);
            if (Ended) DrawEndOverlay(w);
        }

        void DrawBattlefield()
        {
            float sd = Time.time - shakeT;
            camShake = sd < 0.25f
                ? new Vector2(Mathf.Round(Random.Range(-1f, 1f) * shakeMag * (1f - sd / 0.25f)), Mathf.Round(Random.Range(-1f, 1f) * shakeMag * (1f - sd / 0.25f)))
                : Vector2.zero;

            DrawSquare(new Rect(0, 0, Screen.width, Screen.height), new Color(0.07f, 0.07f, 0.12f));
            var bd = Tex("Battle/backdrop");
            if (bd != null)
            {
                // bờ đất của nền (dòng BackdropGround) nằm trên chỗ đứng 10 pixel
                float bx = Mathf.Round((viewW - bd.width) / 2f), by = GroundY - 10 - BackdropGround;
                DrawSquare(ViewToScreen(new Rect(-4, by + BackdropGround, viewW + 8, viewH)), new Color(0.2f, 0.18f, 0.2f));
                GUI.DrawTexture(ViewToScreen(new Rect(bx, by, bd.width, bd.height)), bd);
            }

            var all = new List<Combatant>(ctx.Allies);
            all.AddRange(ctx.Enemies);
            all.Sort((a, b) => SlotPos(a).y.CompareTo(SlotPos(b).y));
            spriteRects.Clear();
            foreach (var c in all) DrawCombatant(c);

            // mũi tên chọn mục tiêu / người đang có lượt (vẽ bằng pixel cho nét)
            var target = TargetedNow();
            float bob = Mathf.Round(Mathf.Sin(Time.time * 6f) * 1.5f);
            if (target != null) PixelArrow(target, Gold, bob);
            else if (current != null && current.IsAlive && !Ended && (MyTurn || phase == Phase.Busy || phase == Phase.Parry))
                PixelArrow(current, current.IsAlly ? Color.white : new Color(1f, 0.45f, 0.4f), bob);
            if (!Ended)
                foreach (var a in ctx.Allies) // người sắp trúng đòn của quái đang ra tay
                    if (a.IsAlive && UnderAttack(a)) PixelArrow(a, new Color(1f, 0.3f, 0.25f), -bob);
        }

        void DrawCombatant(Combatant c)
        {
            bool fb;
            var tex = SpriteFor(c, out fb);
            var slot = SlotPos(c);
            var feet = slot + AnimOffset(c);
            float h = tex == null ? 24f : fb ? 30f : tex.height;
            float wd = tex == null ? 16f : fb ? tex.width * 30f / tex.height : tex.width;
            var r = new Rect(Mathf.Round(feet.x - wd / 2f), feet.y - h + 1, wd, h);
            DrawSquare(ViewToScreen(new Rect(slot.x - 7, slot.y - 1, 14, 3)), new Color(0f, 0f, 0f, c.IsAlive ? 0.35f : 0.15f));
            var sr = ViewToScreen(r);
            spriteRects[c] = sr;
            if (tex == null)
            {
                DrawSquare(sr, c.IsAlive ? c.Color : Color.gray);
                return;
            }
            var old = GUI.color;
            if (!c.IsAlive) GUI.color = c.IsAlly ? new Color(0.45f, 0.45f, 0.5f, 0.85f) : new Color(0.4f, 0.4f, 0.45f, 0.2f);
            else
            {
                float dt = Time.time - AnimOf(c).hitT; // nháy đỏ khi trúng đòn
                GUI.color = dt < HitTime ? Color.Lerp(new Color(1f, 0.35f, 0.35f), Color.white, dt / HitTime) : Color.white;
            }
            GUI.DrawTexture(sr, tex, ScaleMode.StretchToFill);
            GUI.color = old;
        }

        void PixelArrow(Combatant c, Color col, float bob)
        {
            Rect sr;
            if (!spriteRects.TryGetValue(c, out sr)) return;
            float cx = Mathf.Round(sr.center.x / px), top = Mathf.Round(sr.y / px) - 7 + bob;
            for (int row = 0; row < 4; row++)
            {
                int half = 3 - row;
                DrawSquare(new Rect((cx - half - 1) * px, (top + row - 1) * px, (half * 2 + 3) * px, 3 * px), new Color(0.1f, 0.06f, 0.06f));
            }
            for (int row = 0; row < 4; row++)
            {
                int half = 3 - row;
                DrawSquare(new Rect((cx - half) * px, (top + row) * px, (half * 2 + 1) * px, px), col);
            }
        }

        // Tên, máu, ý định cạnh sprite; bấm thẳng vào sprite để chọn mục tiêu.
        void DrawFieldLabels()
        {
            var targeted = TargetedNow();
            bool targeting = MyTurn && pending != Pending.None;
            foreach (var e in ctx.Enemies)
            {
                Rect sr;
                if (!spriteRects.TryGetValue(e, out sr)) continue;
                var g = ToGui(sr);
                var feet = ToGui(ViewToScreen(new Rect(SlotPos(e).x, SlotPos(e).y, 0, 0)));
                if (e.IsAlive)
                {
                    float bw = 110;
                    ShadowLabel(new Rect(feet.x - bw / 2f, feet.y + 6, bw, 20), e.Name, smallCenter);
                    var hb = new Rect(feet.x - bw / 2f, feet.y + 26, bw, 9);
                    DrawBar(hb, (float)e.HP / e.MaxHP, HpColor);
                    int dmg;
                    if (targeting && !TargetsAllies && e == targeted && Preview(e, out dmg) != null && dmg > 0)
                    {
                        // phần máu sắp mất nhấp nháy trắng
                        float lost = Mathf.Min(dmg, e.HP) / (float)e.MaxHP;
                        float al = Mathf.Repeat(Time.time, 0.6f) < 0.3f ? 0.9f : 0.4f;
                        DrawSquare(new Rect(hb.x + hb.width * ((float)e.HP / e.MaxHP - lost), hb.y, hb.width * lost, hb.height), new Color(1f, 1f, 1f, al));
                    }
                    GUI.Label(new Rect(feet.x - bw / 2f, feet.y + 36, bw, 18), e.HP + "/" + e.MaxHP, smallCenter);
                    DrawIntentBubble(e, g);
                }
                if (targeting && !TargetsAllies && e.IsAlive)
                {
                    var hit = new Rect(g.x - 12, g.y - 12, g.width + 24, g.height + 60);
                    if (GUI.Button(hit, GUIContent.none, GUIStyle.none)) ConfirmTarget(e);
                }
            }
            foreach (var a in ctx.Allies)
            {
                Rect sr;
                if (!spriteRects.TryGetValue(a, out sr)) continue;
                var g = ToGui(sr);
                var feet = ToGui(ViewToScreen(new Rect(SlotPos(a).x, SlotPos(a).y, 0, 0)));
                float bw = 64;
                DrawBar(new Rect(feet.x - bw / 2f, feet.y + 8, bw, 6), (float)a.HP / a.MaxHP, HpColor);
                float ix = g.center.x - 10; // biểu tượng trạng thái trên đầu
                if (a.Shield > 0) { DrawIcon("shield", new Rect(ix, g.y - 26, 20, 20)); ix += 22; }
                if (a.Possessed || a.PossessedPending) DrawIcon("amkhi", new Rect(ix, g.y - 26, 20, 20));
                if (a.Guarding) ShadowLabel(new Rect(g.x - 20, g.y - 46, g.width + 40, 20), "Đỡ", smallCenter);
                if (targeting && TargetsAllies && a.IsAlive)
                {
                    var hit = new Rect(g.x - 12, g.y - 12, g.width + 24, g.height + 40);
                    if (GUI.Button(hit, GUIContent.none, GUIStyle.none)) ConfirmTarget(a);
                }
            }
        }

        void DrawIntentBubble(Combatant e, Rect g)
        {
            if (e.Intent == null) return;
            var it = e.Intent;
            string icon = it.type == IntentType.Terrify ? "terrify" : it.type == IntentType.AllHit ? "all" : "single";
            string body;
            if (it.type == IntentType.Terrify) body = "+" + it.power + " Âm khí cả đội";
            else if (it.type == IntentType.AllHit) body = it.power + " cả đội";
            else body = it.power + " → " + (e.IntentTargets.Count > 0 ? e.IntentTargets[0].Name : "?");
            string head = e.IntentCanceled ? "Đã hủy" : it.label;
            var st = e.IntentCanceled ? intentDimStyle : intentStyle;
            float tw = Mathf.Max(st.CalcSize(new GUIContent(head)).x, smallStyle.CalcSize(new GUIContent(body)).x);
            float lift = (ctx.Enemies.IndexOf(e) % 2) * 54f; // xếp so le để bong bóng cạnh nhau không đè
            var r = new Rect(g.center.x - (tw + 44) / 2f, g.y - 62 - lift, tw + 44, 50);
            if (plaqueSt != null) GUI.Box(r, GUIContent.none, plaqueSt);
            else DrawSquare(r, new Color(0.1f, 0.08f, 0.1f, 0.9f));
            var old = GUI.color;
            if (e.IntentCanceled) GUI.color = new Color(1f, 1f, 1f, 0.4f);
            DrawIcon(icon, new Rect(r.x + 8, r.y + 13, 22, 22));
            GUI.color = old;
            GUI.Label(new Rect(r.x + 36, r.y + 5, tw + 4, 22), head, st);
            GUI.Label(new Rect(r.x + 36, r.y + 25, tw + 4, 20), body, e.IntentCanceled ? descStyle : smallStyle);
            if (e.IntentCanceled) DrawSquare(new Rect(r.x + 34, r.y + 35, tw + 4, 2), new Color(0.8f, 0.8f, 0.85f, 0.7f));
            // đuôi bong bóng chỉ xuống đầu quái
            DrawSquare(new Rect(g.center.x - 4, r.yMax - 2, 8, 4), new Color(0.12f, 0.09f, 0.1f));
            DrawSquare(new Rect(g.center.x - 1, r.yMax + 2, 2, 8 + lift), new Color(0.12f, 0.09f, 0.1f, 0.8f));
        }

        void DrawIcon(string name, Rect r)
        {
            var t = Tex("Battle/icon_" + name);
            if (t != null) GUI.DrawTexture(r, t);
        }

        // Thứ tự lượt: ô hình đầu từng người, người đang đi nhô lên viền vàng.
        void DrawTopBar(float w)
        {
            var rb = new Rect(16, 10, 92, 52);
            Box(rb);
            ShadowLabel(new Rect(rb.x, rb.y + 4, rb.width, 20), "VÒNG", smallCenter);
            ShadowLabel(new Rect(rb.x, rb.y + 20, rb.width, 30), round.ToString(), bigNumStyle);

            float x = 118;
            for (int i = 0; i < turnQueue.Count; i++)
            {
                var c = turnQueue[i];
                bool isCurrent = c == current && !Ended;
                bool done = i < turnIndex && !isCurrent;
                var r = new Rect(x, isCurrent ? 8 : 14, 48, 48);
                Box(r);
                var old = GUI.color;
                GUI.color = !c.IsAlive ? new Color(0.3f, 0.3f, 0.3f, 0.6f) : done ? new Color(1f, 1f, 1f, 0.35f) : Color.white;
                DrawHead(c, new Rect(r.x + 6, r.y + 6, 36, 36));
                GUI.color = old;
                DrawSquare(new Rect(r.x + 6, r.yMax - 9, 36, 3), c.IsAlly ? new Color(0.45f, 0.75f, 1f) : new Color(1f, 0.4f, 0.35f));
                if (isCurrent) Outline(r, Gold, 3f);
                x += 54;
            }
            GUI.Label(new Rect(x + 6, 24, 120, 22), "→ vòng sau", descStyle);

            if (DayMode)
            {
                ShadowLabel(new Rect(w - 316, 18, 300, 26), "Điện Thoải phủ · Trận " + (encounter + 1), rightSmallStyle);
                return;
            }
            if (GUI.Button(new Rect(w - 150, 14, 134, 38), "Chơi lại (R)", btnSt)) BuildBattle();
            if (GUI.Button(new Rect(w - 296, 14, 138, 38), "Trận " + (encounter + 1) + "/2 (T)", btnSt)) SwitchEncounter();
        }

        // Hình đầu: phần trên sprite đi (đội) hoặc sprite quái.
        void DrawHead(Combatant c, Rect r)
        {
            string key = SpriteKey(c.Name);
            var t = c.IsAlly ? Tex("Walk/" + key + "_down_0") : Tex("Battle/" + key + "_0");
            if (t == null)
            {
                DrawSquare(r, c.Color);
                return;
            }
            float frac = c.IsAlly ? 15f / 36f : 0.6f;
            var uv = new Rect(0, 1f - frac, 1, frac);
            float aspect = t.width / (t.height * frac);
            float hh = r.height, ww = hh * aspect;
            if (ww > r.width) { ww = r.width; hh = ww / aspect; }
            GUI.DrawTextureWithTexCoords(new Rect(r.center.x - ww / 2f, r.center.y - hh / 2f, ww, hh), t, uv);
        }

        // Dòng thông báo giữa trên: mô tả lệnh, cách chọn mục tiêu, ai đang đánh.
        void DrawMessage(float w)
        {
            string line;
            if (MyTurn && pending != Pending.None)
            {
                var t = TargetedNow();
                int dmg;
                line = t != null ? current.Name + " → " + t.Name + ": " + Preview(t, out dmg) + "    ←/→ đổi · Enter · Esc"
                                 : "Chọn mục tiêu    ←/→ đổi · Enter · Esc";
            }
            else if (MyTurn && itemMenu)
                line = !string.IsNullOrEmpty(message) ? message
                    : itemIndex >= 0 && itemIndex < items.Length ? items[itemIndex].Description : "";
            else if (MyTurn)
                line = !string.IsNullOrEmpty(message) ? message : MenuDescription(menuIndex);
            else if (phase == Phase.Parry)
                line = parryLabel + " ra đòn! Bấm Space khi vạch trắng vào vùng đỏ để gạt.";
            else if (phase == Phase.Timing)
                line = current.CharData.ultiName + " · đòn " + ultiHit + "/" + balance.ultiHits + ": bấm Space khi vạch vào vùng vàng.";
            else if (phase == Phase.Busy && current != null && (!current.IsAlly || current.Possessed))
                line = current.Possessed ? current.Name + " bị nhập, đánh đồng đội…" : current.Name + " đang hành động…";
            else line = "";
            if (string.IsNullOrEmpty(line) || Ended) return;
            var size = hintStyle.CalcSize(new GUIContent(line));
            var r = new Rect(w / 2f - size.x / 2f - 18, 72, size.x + 36, 34);
            if (plaqueSt != null) GUI.Box(r, GUIContent.none, plaqueSt);
            GUI.Label(new Rect(r.x + 18, r.y + 7, size.x + 4, 22), line, hintStyle);
        }

        // Xem trước kết quả lệnh lên mục tiêu (chưa tính né và crit ngẫu nhiên). dmg = sát thương ước tính lên quái.
        string Preview(Combatant t, out int dmg)
        {
            dmg = 0;
            var d = current.CharData;
            switch (pending)
            {
                case Pending.Attack:
                    dmg = Mathf.Max(1, current.Attack - t.Defense);
                    return "~" + dmg + " sát thương · crit " + CombatRules.CritChance(current, 0, balance) + "%";
                case Pending.Skill:
                    if (d.skillType == SkillType.PowerStrike)
                    {
                        dmg = Mathf.Max(1, Mathf.RoundToInt(current.Attack * d.skillPower) - t.Defense);
                        return d.skillName + " ~" + dmg + " sát thương";
                    }
                    if (d.skillType == SkillType.Shield) return "Khiên " + Mathf.RoundToInt(d.skillPower) + " (không cộng dồn)";
                    return t.Intent != null && !t.IntentCanceled ? "hủy \"" + t.Intent.label + "\"" : "không còn ý định để hủy";
                case Pending.Ulti:
                {
                    int per = Mathf.Max(1, Mathf.RoundToInt(current.Attack * balance.ultiDamageMultiplier) - t.Defense);
                    dmg = per * balance.ultiHits;
                    return balance.ultiHits + " đòn × ~" + per + ", bấm nhịp để tăng crit";
                }
                case Pending.Item:
                {
                    var it = items[selectedItem];
                    if (it.effect == ItemEffect.Talisman)
                    {
                        dmg = it.power;
                        return it.displayName + " " + it.power + " sát thương, bỏ qua Thủ và né";
                    }
                    if (it.effect == ItemEffect.HealHP) return it.displayName + " +" + Mathf.Min(it.power, t.MaxHP - t.HP) + " HP";
                    return it.displayName + " -" + Mathf.Min(it.power, t.AmKhi) + " Âm khí";
                }
            }
            return "";
        }

        // Người đang bị quái đánh ngay lúc này (để thẻ và sprite nháy đỏ).
        bool UnderAttack(Combatant a)
        {
            if (current == null || current.IsAlly || current.Intent == null || current.IntentCanceled) return false;
            if (phase != Phase.Parry && phase != Phase.Busy) return false;
            return current.IntentTargets.Contains(a);
        }

        struct Chip
        {
            public string icon, text;
            public Color col;
        }

        // Trạng thái và đòn sắp nhận, dạng ô nhỏ có icon.
        List<Chip> Chips(Combatant a)
        {
            var list = new List<Chip>();
            var purple = new Color(0.75f, 0.5f, 1f);
            var blue = new Color(0.55f, 0.78f, 1f);
            if (!a.IsAlive)
            {
                list.Add(new Chip { text = "Đã gục", col = new Color(0.6f, 0.6f, 0.62f) });
                return list;
            }
            if (a.Possessed) list.Add(new Chip { icon = "amkhi", text = "Bị nhập → " + (a.PossessionTarget != null ? a.PossessionTarget.Name : "?"), col = purple });
            else if (a.PossessedPending) list.Add(new Chip { icon = "amkhi", text = "Sắp bị nhập", col = purple });
            if (a.Guarding) list.Add(new Chip { icon = "shield", text = "Đỡ -" + Mathf.RoundToInt(balance.guardReduction * 100) + "%", col = blue });
            if (a.Shield > 0) list.Add(new Chip { icon = "shield", text = "Khiên " + a.Shield, col = blue });
            foreach (var e in ctx.Enemies)
            {
                if (!e.IsAlive || e.Intent == null || e.IntentCanceled || !e.IntentTargets.Contains(a)) continue;
                var it = e.Intent;
                if (it.type == IntentType.Terrify)
                    list.Add(new Chip { icon = "terrify", text = "+" + it.power + " Âm khí", col = purple });
                else
                    list.Add(new Chip { icon = it.type == IntentType.AllHit ? "all" : "single", text = it.power + " · " + e.Name, col = new Color(1f, 0.5f, 0.42f) });
            }
            return list;
        }

        void DrawChips(Rect area, List<Chip> chips)
        {
            float x = area.x, y = area.y;
            foreach (var c in chips)
            {
                var size = chipStyle.CalcSize(new GUIContent(c.text));
                float cw = size.x + (c.icon != null ? 30 : 14);
                if (x + cw > area.xMax && x > area.x)
                {
                    x = area.x;
                    y += 24;
                }
                if (y + 20 > area.yMax) break;
                var r = new Rect(x, y, cw, 21);
                DrawSquare(r, new Color(0.07f, 0.05f, 0.07f, 0.92f));
                DrawSquare(new Rect(r.x, r.y, 3, r.height), c.col);
                float tx = r.x + 8;
                if (c.icon != null)
                {
                    DrawIcon(c.icon, new Rect(r.x + 7, r.y + 2, 17, 17));
                    tx += 18;
                }
                var old = chipStyle.normal.textColor;
                chipStyle.normal.textColor = c.col;
                GUI.Label(new Rect(tx, r.y + 2, size.x + 4, 18), c.text, chipStyle);
                chipStyle.normal.textColor = old;
                x += cw + 6;
            }
        }

        // Một dòng chỉ số trên thẻ: icon, thanh, số bên phải.
        void StatRow(float x, float y, float w, string icon, float t, Color col, string value)
        {
            const float valW = 62;
            DrawIcon(icon, new Rect(x, y - 3, 16, 16));
            DrawBar(new Rect(x + 21, y, w - 21 - valW - 4, 10), t, col);
            GUI.Label(new Rect(x + w - valW, y - 5, valW, 20), value, barTextStyle);
        }

        void DrawLog()
        {
            int count = Mathf.Min(3, ctx.Log.Count);
            if (count == 0) return;
            var r = new Rect(16, 118, 430, 8 + count * 18);
            DrawSquare(r, new Color(0.05f, 0.04f, 0.07f, 0.55f));
            for (int i = 0; i < count; i++)
                GUI.Label(new Rect(r.x + 10, r.y + 4 + i * 18, r.width - 16, 20), ctx.Log[ctx.Log.Count - count + i],
                    i == count - 1 ? smallStyle : descStyle);
        }

        // Thẻ đội phía dưới: chân dung, HP, MP, Nộ, Âm khí, trạng thái.
        void DrawCards(float w)
        {
            int n = ctx.Allies.Count;
            if (n == 0) return;
            const float x0 = 330, gap = 12, y0 = 552, ch = 158;
            float cw = (w - x0 - 16 - gap * (n - 1)) / n;
            var targeted = TargetedNow();
            bool targeting = MyTurn && pending != Pending.None && TargetsAllies;
            for (int i = 0; i < n; i++)
            {
                var a = ctx.Allies[i];
                bool cur = a == current && !Ended;
                var r = new Rect(x0 + i * (cw + gap), y0 - (cur ? 10 : 0), cw, ch);
                Box(r);
                if (cur) Outline(r, Gold, 3f);
                if (targeting && a == targeted) Outline(r, new Color(0.55f, 0.9f, 1f), 3f);
                if (UnderAttack(a)) // đang bị đánh: viền đỏ nhấp nháy
                    Outline(r, new Color(1f, 0.3f, 0.25f, Mathf.Repeat(Time.time, 0.4f) < 0.2f ? 1f : 0.4f), 4f);

                var pr = new Rect(r.x + 12, r.y + 12, 58, 58);
                DrawSquare(pr, new Color(0.2f, 0.17f, 0.24f));
                var oldc = GUI.color;
                if (!a.IsAlive) GUI.color = new Color(0.5f, 0.5f, 0.5f, 0.8f);
                if (a.CharData.portrait != null) GUI.DrawTexture(pr, a.CharData.portrait, ScaleMode.ScaleToFit);
                GUI.color = oldc;

                float tx = r.x + 80, tw = r.width - 92;
                ShadowLabel(new Rect(tx, r.y + 8, tw, 24), a.Name, nameStyle);
                string role = a.CharData.role;
                GUI.Label(new Rect(tx, r.y + 11, tw, 20), string.IsNullOrEmpty(role) ? "Tốc " + a.Speed + " · Crit " + a.Crit + "%" : role,
                    string.IsNullOrEmpty(role) ? rightSmallStyle : roleStyle);

                float hpT = (float)a.HP / a.MaxHP;
                bool low = a.IsAlive && hpT < 0.3f && Mathf.Repeat(Time.time, 0.8f) < 0.4f; // máu thấp: nháy
                StatRow(tx, r.y + 39, tw, "heart", hpT, low ? new Color(1f, 0.55f, 0.5f) : HpColor, a.HP + "/" + a.MaxHP);

                // MP: các ô, mỗi ô 1 điểm; ô đủ cho 1 skill thì sáng hơn
                const float valW = 62;
                DrawIcon("mana", new Rect(tx, r.y + 54, 16, 16));
                float pw = (tw - 21 - valW - 4) / balance.manaMax;
                for (int m = 0; m < balance.manaMax; m++)
                {
                    var pip = new Rect(tx + 21 + m * pw, r.y + 57, pw - 2, 10);
                    DrawSquare(pip, new Color(0.1f, 0.1f, 0.14f));
                    if (m < a.Mana) DrawSquare(new Rect(pip.x + 1, pip.y + 1, pip.width - 2, pip.height - 2), ManaColor);
                }
                GUI.Label(new Rect(tx + tw - valW, r.y + 52, valW, 20), a.Mana + "/" + balance.manaMax, barTextStyle);

                bool full = a.Rage >= balance.rageMax;
                StatRow(tx, r.y + 75, tw, "rage", (float)a.Rage / balance.rageMax,
                    full ? (Mathf.Repeat(Time.time, 0.6f) < 0.3f ? Gold : new Color(1f, 0.95f, 0.6f)) : RageColor,
                    full ? "ĐẦY" : a.Rage + "/" + balance.rageMax);

                StatRow(tx, r.y + 93, tw, "amkhi", (float)a.AmKhi / balance.amKhiMax, AmKhiColor,
                    a.AmKhi + (a.HasConflict ? " ×" + balance.conflictMultiplier : ""));

                DrawChips(new Rect(r.x + 12, r.y + 110, r.width - 24, 46), Chips(a));
                if (targeting && a.IsAlive && GUI.Button(r, GUIContent.none, GUIStyle.none)) ConfirmTarget(a);
            }
        }

        // Menu lệnh góc trái dưới.
        void DrawCommandMenu()
        {
            if (itemMenu)
            {
                DrawItemMenu();
                return;
            }
            var r = new Rect(16, 536, 300, 176);
            Box(r);
            ShadowLabel(new Rect(r.x + 14, r.y + 8, r.width - 28, 24), current.Name, nameStyle);
            GUI.Label(new Rect(r.x + 14, r.y + 11, r.width - 28, 20), "↑↓ · Enter", rightSmallStyle);
            int n = MenuBase.Length;
            for (int i = 0; i < n; i++)
            {
                var ir = new Rect(r.x + 8, r.y + 36 + i * 22, r.width - 16, 22);
                bool sel = i == menuIndex;
                bool ok = MenuEnabled(i);
                if (sel) DrawSquare(ir, new Color(1f, 0.85f, 0.3f, 0.2f));
                if (sel) DrawSquare(new Rect(ir.x, ir.y, 3, ir.height), Gold);
                var st = ok ? (sel ? menuSelStyle : menuStyle) : menuDisabledStyle;
                string[] menuIcons = { "single", "shield", "mana", "rage", "heart", null };
                var oldc = GUI.color;
                if (!ok) GUI.color = new Color(1f, 1f, 1f, 0.35f);
                if (menuIcons[i] != null) DrawIcon(menuIcons[i], new Rect(ir.x + 10, ir.y + 3, 16, 16));
                GUI.color = oldc;
                GUI.Label(new Rect(ir.x + 32, ir.y + 1, ir.width - 110, ir.height), MenuLabel(i), st);
                GUI.Label(new Rect(ir.xMax - 84, ir.y + 3, 78, ir.height), MenuCost(i), ok ? rightSmallStyle : menuDisabledSmall);
                if (GUI.Button(ir, GUIContent.none, GUIStyle.none))
                {
                    menuIndex = i;
                    Choose(i);
                }
            }
        }

        void DrawItemMenu()
        {
            var r = new Rect(16, 536, 300, 176);
            Box(r);
            ShadowLabel(new Rect(r.x + 14, r.y + 8, r.width - 28, 24), "Đồ", nameStyle);
            GUI.Label(new Rect(r.x + 14, r.y + 11, r.width - 28, 20), "Esc: quay lại", rightSmallStyle);
            for (int i = 0; i < items.Length; i++)
            {
                var ir = new Rect(r.x + 8, r.y + 36 + i * 32, r.width - 16, 30);
                bool sel = i == itemIndex;
                bool ok = bag[i] > 0;
                if (sel) DrawSquare(ir, new Color(1f, 0.85f, 0.3f, 0.2f));
                if (sel) DrawSquare(new Rect(ir.x, ir.y, 3, ir.height), Gold);
                if (items[i].icon != null)
                {
                    var old = GUI.color;
                    GUI.color = ok ? Color.white : new Color(1f, 1f, 1f, 0.35f);
                    GUI.DrawTexture(new Rect(ir.x + 8, ir.y + 1, 28, 28), items[i].icon, ScaleMode.ScaleToFit);
                    GUI.color = old;
                }
                var st = ok ? (sel ? menuSelStyle : menuStyle) : menuDisabledStyle;
                GUI.Label(new Rect(ir.x + 44, ir.y + 4, ir.width - 90, ir.height), items[i].displayName, st);
                GUI.Label(new Rect(ir.xMax - 48, ir.y + 6, 42, ir.height), "x" + bag[i], ok ? rightSmallStyle : menuDisabledSmall);
                if (GUI.Button(ir, GUIContent.none, GUIStyle.none))
                {
                    itemIndex = i;
                    ChooseItem(i);
                }
            }
        }

        // Khi không phải lượt chọn lệnh: ô menu cho biết ai đang đi.
        void DrawWaitPanel()
        {
            if (Ended) return;
            var r = new Rect(16, 536, 300, 176);
            Box(r);
            string who = current != null ? current.Name : "";
            string sub;
            if (MyTurn && pending != Pending.None) sub = "Đang chọn mục tiêu. Bấm vào sprite hoặc thẻ, hoặc dùng ←/→.";
            else if (phase == Phase.Parry) sub = "Chuẩn bị gạt đòn!";
            else if (phase == Phase.Timing) sub = "Bấm theo nhịp!";
            else sub = current != null && !current.IsAlly ? "Lượt của quái." : "";
            ShadowLabel(new Rect(r.x + 14, r.y + 10, r.width - 28, 24), who, nameStyle);
            GUI.Label(new Rect(r.x + 14, r.y + 40, r.width - 28, 120), sub, descStyle);
        }

        void DrawTimingBar(float w, float cursor, float zone, float zoneWidth, Color zoneColor, bool isParry)
        {
            const float pw = 600, ph = 86;
            var panel = new Rect((w - pw) / 2f, 236, pw, ph);
            Box(panel);
            string head = isParry ? "GẠT ĐÒN" : "TUYỆT KỸ · đòn " + ultiHit + "/" + balance.ultiHits;
            ShadowLabel(new Rect(panel.x, panel.y + 8, pw, 24), head, centerStyle);
            var bar = new Rect(panel.x + 30, panel.y + 46, pw - 60, 20);
            DrawSquare(new Rect(bar.x - 2, bar.y - 2, bar.width + 4, bar.height + 4), new Color(0.05f, 0.04f, 0.05f));
            DrawSquare(bar, new Color(0.2f, 0.19f, 0.22f));

            float half = zoneWidth * 0.5f;
            float z0 = Mathf.Clamp01(zone - half), z1 = Mathf.Clamp01(zone + half);
            var fill = zoneColor;
            fill.a = 0.6f;
            DrawSquare(new Rect(bar.x + bar.width * z0, bar.y, bar.width * (z1 - z0), bar.height), fill);
            DrawSquare(new Rect(bar.x + bar.width * zone - 1.5f, bar.y - 4, 3, bar.height + 8), zoneColor);
            DrawSquare(new Rect(bar.x + bar.width * cursor - 4f, bar.y - 8, 8, bar.height + 16), new Color(0.05f, 0.04f, 0.05f));
            DrawSquare(new Rect(bar.x + bar.width * cursor - 2f, bar.y - 6, 4, bar.height + 12), Color.white);

            // Bấm chuột bất kỳ đâu cũng tính là bấm
            if (GUI.Button(new Rect(0, 0, w, 720), GUIContent.none, GUIStyle.none))
            {
                if (isParry) ResolveParry(true);
                else ResolveTiming();
            }
        }

        void Flash(string text, Color c)
        {
            flashText = text;
            flashColor = c;
            flashT = Time.time;
        }

        // Chữ to giữa sân sau mỗi lần bấm nhịp.
        void DrawFlash(float w)
        {
            float t = (Time.time - flashT) / 0.9f;
            if (t >= 1f || string.IsNullOrEmpty(flashText)) return;
            float a = t < 0.7f ? 1f : 1f - (t - 0.7f) / 0.3f;
            float pop = t < 0.12f ? 1.3f - t * 2.5f : 1f;
            bigStyle.fontSize = Mathf.RoundToInt(40 * pop);
            var r = new Rect(0, 176 - t * 20f, w, 60);
            OutlinedLabel(r, flashText, bigStyle, new Color(flashColor.r, flashColor.g, flashColor.b, a), a);
            bigStyle.fontSize = 48;
        }

        void DrawIntro(float w)
        {
            float t = (Time.time - startT) / 1.8f;
            if (t >= 1f) return;
            float a = t < 0.75f ? 1f : 1f - (t - 0.75f) / 0.25f;
            var old = GUI.color;
            GUI.color = new Color(1f, 1f, 1f, a);
            var r = new Rect(w / 2f - 230, 190, 460, 90);
            Box(r);
            OutlinedLabel(new Rect(r.x, r.y + 12, r.width, 40), "Đêm · Điện Thoải phủ", centerBigStyle, new Color(Cream.r, Cream.g, Cream.b, a), a);
            OutlinedLabel(new Rect(r.x, r.y + 52, r.width, 26), "Trận " + (encounter + 1), centerStyle, new Color(Gold.r, Gold.g, Gold.b, a), a);
            GUI.color = old;
        }

        void DrawEndOverlay(float w)
        {
            DrawSquare(new Rect(0, 0, w, 720), new Color(0f, 0f, 0f, 0.55f));
            bool won = phase == Phase.Victory;
            var r = new Rect(w / 2f - 230, 220, 460, 230);
            Box(r);
            OutlinedLabel(new Rect(r.x, r.y + 18, r.width, 56), won ? "THẮNG" : "THUA", bigStyle,
                won ? Gold : new Color(1f, 0.4f, 0.35f), 1f);
            GUI.Label(new Rect(r.x + 30, r.y + 84, r.width - 60, 22), won ? "Ma đã tan. Trời sắp sáng." : "Cả đội gục.", centerStyle);
            var left = new List<string>();
            for (int i = 0; i < items.Length; i++) left.Add(items[i].displayName + " x" + bag[i]);
            GUI.Label(new Rect(r.x + 30, r.y + 114, r.width - 60, 44), "Còn lại: " + string.Join(" · ", left.ToArray()), descCenterStyle);
            var b = new Rect(r.center.x - 100, r.yMax - 64, 200, 44);
            if (DayMode)
            {
                if (GUI.Button(b, "Về làng", btnSt))
                {
                    var bagLeft = BagByName();
                    Hide();
                    OnFinished(won, bagLeft);
                }
                return;
            }
            if (GUI.Button(b, "Chơi lại (R)", btnSt)) BuildBattle();
        }

        // ---------- Hoạt ảnh: thở, lao lên khi đánh, rung khi trúng đòn, số bay ----------

        class Anim
        {
            public float actT = -9f, hitT = -9f, dodgeT = -9f;
            public bool critHit;
        }

        class Popup
        {
            public Combatant target;
            public string text;
            public Color color;
            public float t0, stack;
            public bool big;
        }

        const float ActTime = 0.35f, HitTime = 0.4f, DodgeTime = 0.35f, PopupTime = 1.0f;

        readonly Dictionary<Combatant, Anim> anims = new Dictionary<Combatant, Anim>();
        readonly List<Popup> popups = new List<Popup>();
        readonly Dictionary<Combatant, Rect> spriteRects = new Dictionary<Combatant, Rect>(); // pixel màn hình
        GUIStyle popupStyle, popupBigStyle;

        void OnEnable() { CombatRules.Fx += OnFx; }
        void OnDisable() { CombatRules.Fx -= OnFx; }

        Anim AnimOf(Combatant c)
        {
            Anim a;
            if (!anims.TryGetValue(c, out a)) { a = new Anim(); anims[c] = a; }
            return a;
        }

        void Act(Combatant c)
        {
            if (c != null) AnimOf(c).actT = Time.time;
        }

        void Shake(float mag)
        {
            shakeT = Time.time;
            shakeMag = mag;
        }

        void OnFx(Combatant target, FxKind kind, int amount)
        {
            var an = AnimOf(target);
            switch (kind)
            {
                case FxKind.Damage:
                    an.hitT = Time.time; an.critHit = false;
                    AddPopup(target, "-" + amount, Color.white, false);
                    if (target.IsAlly) Shake(1.5f);
                    break;
                case FxKind.Crit:
                    an.hitT = Time.time; an.critHit = true;
                    AddPopup(target, "CRIT -" + amount, Gold, true);
                    Shake(3f);
                    break;
                case FxKind.Dodge: an.dodgeT = Time.time; AddPopup(target, "Né!", new Color(0.55f, 0.9f, 1f), false); break;
                case FxKind.Parry: AddPopup(target, "Gạt!", Gold, true); break;
                case FxKind.Absorbed: AddPopup(target, "Chặn", new Color(0.6f, 0.75f, 0.95f), false); break;
                case FxKind.Heal: AddPopup(target, "+" + amount + " HP", new Color(0.5f, 1f, 0.55f), false); break;
                case FxKind.Cleanse: AddPopup(target, "-" + amount + " Âm khí", new Color(0.85f, 0.75f, 1f), false); break;
                case FxKind.Terrify: an.hitT = Time.time; an.critHit = false; AddPopup(target, "Rợn người", new Color(0.8f, 0.6f, 1f), false); break;
            }
        }

        void AddPopup(Combatant target, string text, Color color, bool big)
        {
            int stack = 0; // nhiều số cùng lúc trên 1 người thì xếp chồng lên nhau
            foreach (var p in popups)
                if (p.target == target && Time.time - p.t0 < 0.3f) stack++;
            popups.Add(new Popup { target = target, text = text, color = color, t0 = Time.time, stack = stack, big = big });
        }

        // Độ lệch theo pixel trận: thở, lao về phía đối thủ, rung khi trúng, nhảy lùi khi né.
        Vector2 AnimOffset(Combatant c)
        {
            var an = AnimOf(c);
            float now = Time.time;
            Vector2 o = Vector2.zero;
            if (!c.IsAlive) return o;

            float seed = (c.Name.GetHashCode() & 255) / 40f;
            if (c.IsAlly && Mathf.Sin(now * 2.2f + seed) < 0f) o.y += 1f;

            float dt = now - an.actT;
            if (dt < ActTime)
            {
                float kk = dt < 0.12f ? dt / 0.12f : 1f - (dt - 0.12f) / (ActTime - 0.12f);
                o.x += (c.IsAlly ? 1f : -1f) * 18f * kk;
            }
            dt = now - an.hitT;
            if (dt < HitTime) o.x += Mathf.Sin(dt * 70f) * (an.critHit ? 3f : 2f) * (1f - dt / HitTime);
            dt = now - an.dodgeT;
            if (dt < DodgeTime)
            {
                float kk = Mathf.Sin(Mathf.PI * dt / DodgeTime);
                o.x += (c.IsAlly ? -1f : 1f) * 10f * kk;
                o.y -= 6f * kk;
            }
            return new Vector2(Mathf.Round(o.x), Mathf.Round(o.y));
        }

        void DrawPopups()
        {
            float now = Time.time;
            popups.RemoveAll(p => now - p.t0 > PopupTime);
            foreach (var p in popups)
            {
                Rect sr;
                if (!spriteRects.TryGetValue(p.target, out sr)) continue;
                var g = ToGui(sr);
                float t = (now - p.t0) / PopupTime;
                float rise = 40f * (1f - (1f - t) * (1f - t));
                var r = new Rect(g.center.x - 90, g.y - 8 - rise - p.stack * 24f, 180, 32);
                float alpha = t < 0.7f ? 1f : 1f - (t - 0.7f) / 0.3f;
                var col = p.color;
                col.a = alpha;
                OutlinedLabel(r, p.text, p.big ? popupBigStyle : popupStyle, col, alpha);
            }
        }

        // Chữ có viền tối 1px quanh 4 phía, đọc được trên mọi nền.
        static void OutlinedLabel(Rect r, string s, GUIStyle st, Color c, float alpha)
        {
            var old = st.normal.textColor;
            st.normal.textColor = new Color(0.06f, 0.04f, 0.06f, alpha * 0.9f);
            for (int dx = -2; dx <= 2; dx += 2)
                for (int dy = -2; dy <= 2; dy += 2)
                    if (dx != 0 || dy != 0) GUI.Label(new Rect(r.x + dx, r.y + dy, r.width, r.height), s, st);
            st.normal.textColor = c;
            GUI.Label(r, s, st);
            st.normal.textColor = old;
        }

        static void ShadowLabel(Rect r, string s, GUIStyle st)
        {
            var old = st.normal.textColor;
            st.normal.textColor = new Color(0f, 0f, 0f, 0.75f);
            GUI.Label(new Rect(r.x + 1, r.y + 1, r.width, r.height), s, st);
            st.normal.textColor = old;
            GUI.Label(r, s, st);
        }

        // ---------- Vẽ ----------

        GUIStyle smallCenter, intentDimStyle, menuSelStyle, menuDisabledSmall, barTextStyle, bigNumStyle, centerBigStyle, descCenterStyle, chipStyle, roleStyle;

        void EnsureStyles()
        {
            if (nameStyle != null) return;
            nameStyle = new GUIStyle(GUI.skin.label) { fontSize = 17, fontStyle = FontStyle.Bold };
            nameStyle.normal.textColor = Cream;
            textStyle = new GUIStyle(GUI.skin.label) { fontSize = 15 };
            textStyle.normal.textColor = Cream;
            smallStyle = new GUIStyle(GUI.skin.label) { fontSize = 13 };
            smallStyle.normal.textColor = new Color(0.88f, 0.84f, 0.74f);
            smallCenter = new GUIStyle(smallStyle) { alignment = TextAnchor.UpperCenter, fontStyle = FontStyle.Bold };
            smallCenter.normal.textColor = Cream;
            rightSmallStyle = new GUIStyle(GUI.skin.label) { fontSize = 13, alignment = TextAnchor.UpperRight };
            rightSmallStyle.normal.textColor = new Color(0.75f, 0.72f, 0.66f);
            intentStyle = new GUIStyle(GUI.skin.label) { fontSize = 15, fontStyle = FontStyle.Bold };
            intentStyle.normal.textColor = Gold;
            intentDimStyle = new GUIStyle(intentStyle);
            intentDimStyle.normal.textColor = new Color(0.6f, 0.6f, 0.65f);
            statusStyle = new GUIStyle(GUI.skin.label) { fontSize = 13, fontStyle = FontStyle.Bold, wordWrap = true };
            statusStyle.normal.textColor = new Color(1f, 0.6f, 0.5f);
            hintStyle = new GUIStyle(GUI.skin.label) { fontSize = 15 };
            hintStyle.normal.textColor = Cream;
            centerStyle = new GUIStyle(GUI.skin.label) { fontSize = 17, fontStyle = FontStyle.Bold, alignment = TextAnchor.UpperCenter };
            centerStyle.normal.textColor = Cream;
            centerBigStyle = new GUIStyle(centerStyle) { fontSize = 26 };
            markerStyle = new GUIStyle(GUI.skin.label) { fontSize = 18, fontStyle = FontStyle.Bold, alignment = TextAnchor.MiddleCenter };
            markerStyle.normal.textColor = Gold;
            menuStyle = new GUIStyle(GUI.skin.label) { fontSize = 16 };
            menuStyle.normal.textColor = Cream;
            menuSelStyle = new GUIStyle(menuStyle) { fontStyle = FontStyle.Bold };
            menuSelStyle.normal.textColor = Gold;
            menuDisabledStyle = new GUIStyle(GUI.skin.label) { fontSize = 16 };
            menuDisabledStyle.normal.textColor = new Color(0.45f, 0.43f, 0.45f);
            menuDisabledSmall = new GUIStyle(rightSmallStyle);
            menuDisabledSmall.normal.textColor = new Color(0.45f, 0.43f, 0.45f);
            descStyle = new GUIStyle(GUI.skin.label) { fontSize = 13, wordWrap = true };
            descStyle.normal.textColor = new Color(0.7f, 0.7f, 0.76f);
            descCenterStyle = new GUIStyle(descStyle) { alignment = TextAnchor.UpperCenter };
            barTextStyle = new GUIStyle(GUI.skin.label) { fontSize = 13, fontStyle = FontStyle.Bold, alignment = TextAnchor.UpperRight };
            barTextStyle.normal.textColor = Cream;
            chipStyle = new GUIStyle(GUI.skin.label) { fontSize = 12, fontStyle = FontStyle.Bold, wordWrap = false };
            roleStyle = new GUIStyle(rightSmallStyle) { fontStyle = FontStyle.Bold };
            roleStyle.normal.textColor = new Color(0.86f, 0.74f, 0.45f);
            bigStyle = new GUIStyle(GUI.skin.label) { fontSize = 48, fontStyle = FontStyle.Bold, alignment = TextAnchor.MiddleCenter };
            bigNumStyle = new GUIStyle(GUI.skin.label) { fontSize = 24, fontStyle = FontStyle.Bold, alignment = TextAnchor.UpperCenter };
            bigNumStyle.normal.textColor = Gold;
            popupStyle = new GUIStyle(GUI.skin.label) { fontSize = 22, fontStyle = FontStyle.Bold, alignment = TextAnchor.MiddleCenter };
            popupBigStyle = new GUIStyle(popupStyle) { fontSize = 28 };
            UiSkin.Build(Tex, out panelSt, out btnSt, out tabOnSt, out plaqueSt, out tipSt);
        }

        void Box(Rect r)
        {
            if (panelSt != null) GUI.Box(r, GUIContent.none, panelSt);
            else DrawSquare(r, new Color(0.12f, 0.12f, 0.14f, 0.95f));
        }

        static void DrawSquare(Rect r, Color c)
        {
            var old = GUI.color;
            GUI.color = new Color(c.r * old.r, c.g * old.g, c.b * old.b, c.a * old.a);
            GUI.DrawTexture(r, Texture2D.whiteTexture);
            GUI.color = old;
        }

        static void DrawBar(Rect r, float t, Color c)
        {
            DrawSquare(new Rect(r.x - 1, r.y - 1, r.width + 2, r.height + 2), new Color(0.04f, 0.03f, 0.05f));
            DrawSquare(r, new Color(0.18f, 0.16f, 0.2f));
            float fw = r.width * Mathf.Clamp01(t);
            DrawSquare(new Rect(r.x, r.y, fw, r.height), c);
            DrawSquare(new Rect(r.x, r.y, fw, Mathf.Max(1f, r.height * 0.3f)), new Color(1f, 1f, 1f, 0.25f));
        }

        static void Outline(Rect r, Color c, float t)
        {
            DrawSquare(new Rect(r.x, r.y, r.width, t), c);
            DrawSquare(new Rect(r.x, r.yMax - t, r.width, t), c);
            DrawSquare(new Rect(r.x, r.y, t, r.height), c);
            DrawSquare(new Rect(r.xMax - t, r.y, t, r.height), c);
        }
    }
}
