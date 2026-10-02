using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    public enum FxKind { Damage, Crit, Dodge, Parry, Absorbed, Terrify, Heal, Cleanse }

    // Luật tính toán dùng chung cho cả người chơi và quái.
    public static class CombatRules
    {
        // UI nghe sự kiện này để hiện số bay, rung, nháy đỏ. Luật không phụ thuộc UI.
        public static event System.Action<Combatant, FxKind, int> Fx;

        public static void RaiseFx(Combatant target, FxKind kind, int amount)
        {
            if (Fx != null) Fx(target, kind, amount);
        }

        public static int CritChance(Combatant c, int bonusPercent, BalanceConfig cfg)
        {
            return Mathf.Min(cfg.critCap, c.Crit + Mathf.RoundToInt(c.Luck * cfg.luckCritPerPoint) + bonusPercent);
        }

        public static int DodgeChance(Combatant c, BalanceConfig cfg)
        {
            return Mathf.Min(cfg.dodgeCap, c.Dodge + Mathf.RoundToInt(c.Luck * cfg.luckDodgePerPoint));
        }

        public static int RollCrit(Combatant attacker, int damage, int bonusPercent, BalanceConfig cfg,
            out bool crit, out int chance)
        {
            chance = CritChance(attacker, bonusPercent, cfg);
            crit = Random.Range(0, 100) < chance;
            return crit ? Mathf.RoundToInt(damage * cfg.critMultiplier) : damage;
        }

        // cursor, zoneCenter trong khoảng 0..1. Sát tâm = timingMaxBonus, mép vùng = timingEdgeBonus, ngoài vùng = 0.
        public static int TimingBonus(float cursor, float zoneCenter, BalanceConfig cfg)
        {
            float half = cfg.timingZoneWidth * 0.5f;
            float d = Mathf.Abs(cursor - zoneCenter);
            if (d > half) return 0;
            return Mathf.RoundToInt(Mathf.Lerp(cfg.timingMaxBonus, cfg.timingEdgeBonus, d / half));
        }

        // Trả về sát thương thực nhận. Né (ẩn) chỉ áp dụng cho đòn đơn mục tiêu.
        public static int Hit(Combatant target, int raw, bool singleTarget, bool crit, string source,
            BalanceConfig cfg, List<string> log)
        {
            if (!target.IsAlive) return 0;

            if (singleTarget && Random.Range(0, 100) < DodgeChance(target, cfg))
            {
                log.Add(target.Name + " né đòn của " + source + ".");
                RaiseFx(target, FxKind.Dodge, 0);
                return 0;
            }

            int dmg = Mathf.Max(1, raw - target.Defense);
            if (target.Guarding)
            {
                dmg = Mathf.CeilToInt(dmg * (1f - cfg.guardReduction));
                target.Guarding = false;
            }
            if (target.Shield > 0)
            {
                int absorbed = Mathf.Min(target.Shield, dmg);
                target.Shield -= absorbed;
                dmg -= absorbed;
            }

            target.HP = Mathf.Max(0, target.HP - dmg);
            log.Add((crit ? "CRIT! " : "") + source + " → " + target.Name + ": -" + dmg + " HP");
            RaiseFx(target, dmg == 0 ? FxKind.Absorbed : (crit ? FxKind.Crit : FxKind.Damage), dmg);

            if (target.IsAlly && dmg > 0)
            {
                target.Rage = Mathf.Min(cfg.rageMax, target.Rage + cfg.ragePerHitTaken);
                AddAmKhi(target, cfg.amKhiOnHit + (crit ? cfg.amKhiOnCrit : 0), cfg, log);
            }

            if (!target.IsAlive) log.Add(target.Name + " gục.");
            return dmg;
        }

        // Một đòn trong Tuyệt kỹ: bonus crit lấy từ thanh căng nhịp.
        public static void UltiHit(Combatant actor, Combatant target, int hitIndex, int timingBonus,
            BalanceConfig cfg, List<string> log)
        {
            if (!target.IsAlive) return;
            bool crit;
            int chance;
            int raw = Mathf.RoundToInt(actor.Attack * cfg.ultiDamageMultiplier);
            int dmg = RollCrit(actor, raw, timingBonus, cfg, out crit, out chance);
            log.Add(actor.Name + " — " + actor.CharData.ultiName + " đòn " + hitIndex + "/" + cfg.ultiHits + ": tỉ lệ crit " + chance + "%");
            Hit(target, dmg, true, crit, actor.Name, cfg, log);
        }

        public static void AddAmKhi(Combatant t, int amount, BalanceConfig cfg, List<string> log)
        {
            if (!t.IsAlly || !t.IsAlive || amount <= 0) return;

            float a = amount * (t.HasConflict ? cfg.conflictMultiplier : 1) * (1f - t.AmKhiResist);
            int add = Mathf.Max(1, Mathf.RoundToInt(a));

            t.AmKhi = Mathf.Min(cfg.amKhiMax, t.AmKhi + add);
            if (t.AmKhi >= cfg.amKhiMax && !t.PossessedPending && !t.Possessed)
            {
                t.PossessedPending = true;
                log.Add(t.Name + " đầy Âm khí — vòng sau sẽ bị nhập!");
            }
        }
    }
}
