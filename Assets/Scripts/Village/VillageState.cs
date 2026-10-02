using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    public class PlotState
    {
        public int crop = -1;   // chỉ số trong cfg.crops, -1 = trống
        public int plantedDay;
    }

    // Trạng thái làng: logic thuần, không vẽ gì. DayController chỉ đọc và gọi các hàm này.
    public class VillageState
    {
        public readonly VillageConfig Cfg;
        public int Day = 1, Loop = 1, ActionsLeft;
        public int Rituals;            // số lần sửa đình
        public int Memories;           // số mảnh ký ức đã mở
        public int TonightBonusHp;     // buff món ăn, mất sau đêm
        public readonly List<PlotState> Plots = new List<PlotState>();
        public readonly Dictionary<string, int> Inv = new Dictionary<string, int>();
        public readonly Dictionary<string, int> Affinity = new Dictionary<string, int>();
        public readonly Dictionary<string, int> Bond = new Dictionary<string, int>();
        public readonly List<string> Log = new List<string>();

        public VillageState(VillageConfig cfg)
        {
            Cfg = cfg;
            foreach (var n in cfg.npcs) Affinity[n.name] = 0;
            foreach (var f in cfg.friends) Bond[f] = 0;
            ResetWorld();
            Log.Add("Ngày 1. Cả nhóm về làng dự giỗ Hải.");
        }

        // Vòng lặp chỉ xóa thế giới (ruộng, đồ), không xóa tiến trình (thân thiết, gắn kết, ký ức, đình đã sửa).
        void ResetWorld()
        {
            Plots.Clear();
            for (int i = 0; i < Cfg.plotSlots; i++) Plots.Add(new PlotState());
            Inv.Clear();
            foreach (var s in Cfg.startItems) Add(s.name, s.count);
            ActionsLeft = Cfg.actionsPerDay;
            TonightBonusHp = 0;
        }

        // ---------- túi đồ ----------

        public int Count(string name)
        {
            int n;
            return Inv.TryGetValue(name, out n) ? n : 0;
        }

        public void Add(string name, int n)
        {
            Inv[name] = Count(name) + n;
        }

        bool HasAll(string[] needs)
        {
            var need = new Dictionary<string, int>();
            foreach (var x in needs) need[x] = (need.ContainsKey(x) ? need[x] : 0) + 1;
            foreach (var kv in need) if (Count(kv.Key) < kv.Value) return false;
            return true;
        }

        bool Spend()
        {
            if (ActionsLeft <= 0) { Log.Add("Hết lượt hôm nay. Đi đêm thôi."); return false; }
            ActionsLeft--;
            return true;
        }

        public bool CanAct
        {
            get { return ActionsLeft > 0; }
        }

        // ---------- ruộng ----------

        public bool IsReady(int slot)
        {
            var p = Plots[slot];
            return p.crop >= 0 && Day - p.plantedDay >= Cfg.crops[p.crop].days;
        }

        public int DaysLeft(int slot)
        {
            var p = Plots[slot];
            return p.crop < 0 ? 0 : Mathf.Max(0, Cfg.crops[p.crop].days - (Day - p.plantedDay));
        }

        public bool Plant(int slot, int crop)
        {
            if (Plots[slot].crop >= 0 || !Spend()) return false;
            Plots[slot].crop = crop;
            Plots[slot].plantedDay = Day;
            Log.Add("Trồng " + Cfg.crops[crop].name + " (chín sau " + Cfg.crops[crop].days + " ngày).");
            return true;
        }

        public bool Harvest(int slot)
        {
            if (!IsReady(slot) || !Spend()) return false;
            var c = Cfg.crops[Plots[slot].crop];
            Add(c.yield, c.yieldCount);
            Plots[slot].crop = -1;
            Log.Add("Thu hoạch " + c.name + ": +" + c.yieldCount + " " + c.yield + ".");
            return true;
        }

        // ---------- nấu ăn, làm đồ ----------

        public bool Unlocked(RecipeDef r)
        {
            return string.IsNullOrEmpty(r.npc) || Affinity[r.npc] >= r.npcLevel;
        }

        public string WhyCannotMake(RecipeDef r)
        {
            if (!Unlocked(r)) return "Cần " + r.npc + " thân thiết mức " + r.npcLevel;
            if (!HasAll(r.needs)) return "Thiếu nguyên liệu";
            if (!CanAct) return "Hết lượt";
            return null;
        }

        public bool Make(RecipeDef r)
        {
            if (WhyCannotMake(r) != null || !Spend()) return false;
            foreach (var x in r.needs) Inv[x] = Count(x) - 1;
            if (r.kind == RecipeKind.Food)
            {
                TonightBonusHp = Mathf.Max(TonightBonusHp, r.foodBonusHp);
                Log.Add("Nấu " + r.output + ". Đêm nay cả đội +" + r.foodBonusHp + " HP tối đa.");
            }
            else
            {
                Add(r.output, 1);
                Log.Add("Làm xong " + r.output + ".");
            }
            return true;
        }

        // ---------- thăm người ----------

        public bool Visit(NpcDef npc)
        {
            if (Affinity[npc.name] >= Cfg.maxAffinity || !Spend()) return false;
            int lv = ++Affinity[npc.name];
            Log.Add("Thăm " + npc.name + ": thân thiết mức " + lv + ". " + npc.levelNotes[lv - 1]);
            return true;
        }

        // ---------- sửa đình ----------

        public int UnlockedShrines
        {
            get { return Mathf.Min(2, 1 + Rituals); } // bản thử có 2 điện = 2 trận
        }

        public string WhyCannotRepair()
        {
            foreach (var x in Cfg.ritualSet) if (Count(x) < 1) return "Thiếu " + x;
            if (!CanAct) return "Hết lượt";
            return null;
        }

        public bool RepairDinh()
        {
            if (WhyCannotRepair() != null || !Spend()) return false;
            foreach (var x in Cfg.ritualSet) Inv[x] = Count(x) - 1;
            Rituals++;
            Log.Add("Dâng lễ sửa đình: khôi phục nghi lễ thứ " + Rituals + "." + (Rituals == 1 ? " Mở trận 2 để đi đêm." : ""));
            return true;
        }

        // ---------- tìm manh mối ----------

        public bool SeekClue(string friend)
        {
            if (!Spend()) return false;
            Bond[friend] = Mathf.Min(Cfg.maxBond, Bond[friend] + 1);
            if (Memories < Cfg.memoryCount)
            {
                Memories++;
                Log.Add("Đi cùng " + friend + ": mở mảnh ký ức " + Memories + "/" + Cfg.memoryCount + ". Gắn kết +1.");
            }
            else Log.Add("Đi cùng " + friend + ": không còn ký ức mới trong bản này. Gắn kết +1.");
            return true;
        }

        // ---------- đêm ----------

        public Dictionary<string, int> BagForNight()
        {
            return new Dictionary<string, int>(Inv);
        }

        public void AfterNight(bool won, Dictionary<string, int> left)
        {
            foreach (var kv in left) Inv[kv.Key] = kv.Value;
            Log.Add(won ? "Đêm qua thắng." : "Đêm qua thua. Sáng ra cả nhóm tỉnh dậy ở nhà.");

            Day++;
            TonightBonusHp = 0;
            if (Day > Cfg.loopDays)
            {
                Day = 1;
                Loop++;
                ResetWorld();
                Log.Add("Vòng lặp quay lại ngày 1 (lần " + Loop + "). Ruộng và đồ mất, ký ức và thân thiết còn.");
                return;
            }
            ActionsLeft = Cfg.actionsPerDay;
            Log.Add("Ngày " + Day + ".");
        }
    }
}
