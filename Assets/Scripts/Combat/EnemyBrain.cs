using System.Collections.Generic;

namespace KyUc
{
    // Quái chọn ý định theo pattern cố định và báo trước mục tiêu.
    public static class EnemyBrain
    {
        public static void PlanIntent(Combatant e, List<Combatant> allies)
        {
            e.Intent = null;
            e.IntentCanceled = false;
            e.IntentTargets.Clear();
            if (!e.IsAlive || e.EnemyData.pattern.Count == 0) return;

            e.Intent = e.EnemyData.pattern[e.PatternIndex % e.EnemyData.pattern.Count];
            e.PatternIndex++;
            e.IntentTargets.AddRange(SelectTargets(e.Intent, allies));
        }

        public static List<Combatant> SelectTargets(IntentDef intent, List<Combatant> allies)
        {
            var alive = allies.FindAll(a => a.IsAlive);
            if (alive.Count == 0) return alive;
            if (intent.type != IntentType.SingleHit || intent.target == TargetRule.All) return alive;

            Combatant best = alive[0];
            foreach (var a in alive)
            {
                if (intent.target == TargetRule.LowestHP)
                {
                    if (a.HP < best.HP) best = a;
                }
                else if (a.AmKhi > best.AmKhi || (a.AmKhi == best.AmKhi && a.HP < best.HP))
                {
                    best = a;
                }
            }
            return new List<Combatant> { best };
        }

        public static bool IsAttack(IntentDef intent)
        {
            return intent != null && (intent.type == IntentType.SingleHit || intent.type == IntentType.AllHit);
        }

        // parried = người chơi gạt đòn thành công: đòn đánh không gây sát thương.
        public static void Execute(Combatant e, BattleContext ctx, bool parried)
        {
            if (!e.IsAlive || e.Intent == null) return;
            if (e.IntentCanceled)
            {
                ctx.Log.Add(e.Name + ": \"" + e.Intent.label + "\" đã bị hủy.");
                return;
            }

            var targets = e.IntentTargets.FindAll(t => t.IsAlive);
            if (targets.Count == 0) targets = SelectTargets(e.Intent, ctx.Allies); // mục tiêu đã gục thì chọn lại theo cùng luật
            if (targets.Count == 0) return;

            var cfg = ctx.Cfg;
            string source = e.Name + " (" + e.Intent.label + ")";

            if (parried && IsAttack(e.Intent))
            {
                foreach (var t in targets)
                {
                    t.Rage = UnityEngine.Mathf.Min(cfg.rageMax, t.Rage + cfg.ragePerParry);
                    CombatRules.RaiseFx(t, FxKind.Parry, 0);
                }
                ctx.Log.Add("Gạt đòn thành công! " + source + " không gây sát thương.");
                return;
            }
            switch (e.Intent.type)
            {
                case IntentType.SingleHit:
                {
                    bool crit;
                    int chance;
                    int dmg = CombatRules.RollCrit(e, e.Intent.power, 0, cfg, out crit, out chance);
                    CombatRules.Hit(targets[0], dmg, true, crit, source, cfg, ctx.Log);
                    break;
                }
                case IntentType.AllHit:
                {
                    bool crit;
                    int chance;
                    int dmg = CombatRules.RollCrit(e, e.Intent.power, 0, cfg, out crit, out chance);
                    foreach (var t in targets) CombatRules.Hit(t, dmg, false, crit, source, cfg, ctx.Log);
                    break;
                }
                case IntentType.Terrify:
                    ctx.Log.Add(source + ": cả đội rợn người");
                    foreach (var t in targets)
                    {
                        CombatRules.AddAmKhi(t, e.Intent.power, cfg, ctx.Log);
                        CombatRules.RaiseFx(t, FxKind.Terrify, e.Intent.power);
                    }
                    break;
            }
        }
    }
}
