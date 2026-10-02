using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    public class BattleContext
    {
        public BalanceConfig Cfg;
        public List<Combatant> Allies = new List<Combatant>();
        public List<Combatant> Enemies = new List<Combatant>();
        public List<string> Log = new List<string>();
    }

    // Command Pattern: mỗi lượt của nhân vật là đúng 1 lệnh.
    public interface ICommand
    {
        bool CanExecute(BattleContext ctx, out string reason);
        void Execute(BattleContext ctx);
    }

    public abstract class AllyCommand : ICommand
    {
        protected readonly Combatant actor;

        protected AllyCommand(Combatant actor)
        {
            this.actor = actor;
        }

        protected abstract bool ValidTarget(BattleContext ctx, out string reason);
        protected abstract void DoAction(BattleContext ctx);

        public bool CanExecute(BattleContext ctx, out string reason)
        {
            reason = null;
            if (!actor.IsAlive) { reason = actor.Name + " đã gục"; return false; }
            if (actor.Possessed) { reason = actor.Name + " đang bị nhập"; return false; }
            return ValidTarget(ctx, out reason);
        }

        public void Execute(BattleContext ctx)
        {
            DoAction(ctx);
        }
    }

    // Đánh thường: crit theo % gốc, hồi mana và tích Nộ.
    public class AttackCommand : AllyCommand
    {
        readonly Combatant target;

        public AttackCommand(Combatant actor, Combatant target) : base(actor)
        {
            this.target = target;
        }

        protected override bool ValidTarget(BattleContext ctx, out string reason)
        {
            reason = null;
            if (target == null || target.IsAlly || !target.IsAlive) { reason = "Chọn một quái còn sống"; return false; }
            return true;
        }

        protected override void DoAction(BattleContext ctx)
        {
            var cfg = ctx.Cfg;
            bool crit;
            int chance;
            int dmg = CombatRules.RollCrit(actor, actor.Attack, 0, cfg, out crit, out chance);
            CombatRules.Hit(target, dmg, true, crit, actor.Name, cfg, ctx.Log);
            actor.Mana = Mathf.Min(cfg.manaMax, actor.Mana + cfg.manaPerAttack);
            actor.Rage = Mathf.Min(cfg.rageMax, actor.Rage + cfg.ragePerAttack);
        }
    }

    // Đỡ: giảm đòn kế tiếp, hết hiệu lực khi đến lượt mình lần sau.
    public class GuardCommand : AllyCommand
    {
        public GuardCommand(Combatant actor) : base(actor) { }

        protected override bool ValidTarget(BattleContext ctx, out string reason)
        {
            reason = null;
            return true;
        }

        protected override void DoAction(BattleContext ctx)
        {
            actor.Guarding = true;
            ctx.Log.Add(actor.Name + " đỡ: đòn kế tiếp giảm " + Mathf.RoundToInt(ctx.Cfg.guardReduction * 100) + "%");
        }
    }

    // Skill: tốn mana.
    public class SkillCommand : AllyCommand
    {
        readonly Combatant target;

        public SkillCommand(Combatant actor, Combatant target) : base(actor)
        {
            this.target = target;
        }

        protected override bool ValidTarget(BattleContext ctx, out string reason)
        {
            reason = null;
            var d = actor.CharData;
            if (actor.Mana < ctx.Cfg.skillManaCost) { reason = "Không đủ mana (cần " + ctx.Cfg.skillManaCost + ")"; return false; }
            if (target == null || !target.IsAlive) { reason = "Chọn mục tiêu còn sống"; return false; }
            if (d.SkillTargetsAlly && !target.IsAlly) { reason = "Chọn một đồng đội"; return false; }
            if (!d.SkillTargetsAlly && target.IsAlly) { reason = "Chọn một quái"; return false; }
            if (d.skillType == SkillType.CancelIntent && (target.Intent == null || target.IntentCanceled))
            {
                reason = "Quái này không còn ý định để hủy";
                return false;
            }
            return true;
        }

        protected override void DoAction(BattleContext ctx)
        {
            var d = actor.CharData;
            actor.Mana -= ctx.Cfg.skillManaCost;
            switch (d.skillType)
            {
                case SkillType.PowerStrike:
                {
                    bool crit;
                    int chance;
                    int raw = Mathf.RoundToInt(actor.Attack * d.skillPower);
                    int dmg = CombatRules.RollCrit(actor, raw, 0, ctx.Cfg, out crit, out chance);
                    CombatRules.Hit(target, dmg, true, crit, actor.Name + " (" + d.skillName + ")", ctx.Cfg, ctx.Log);
                    break;
                }
                case SkillType.CancelIntent:
                    target.IntentCanceled = true;
                    ctx.Log.Add(actor.Name + " hủy ý định \"" + target.Intent.label + "\" của " + target.Name);
                    break;
                case SkillType.Shield:
                {
                    int amount = Mathf.RoundToInt(d.skillPower);
                    target.Shield = Mathf.Max(target.Shield, amount); // không cộng dồn
                    ctx.Log.Add(actor.Name + " che chắn " + target.Name + ": khiên " + amount);
                    break;
                }
            }
        }
    }

    // Tuyệt kỹ: cần Nộ đầy. Lệnh này chỉ trả giá; các đòn đánh do BattleController chạy qua thanh căng nhịp.
    public class UltiCommand : AllyCommand
    {
        readonly Combatant target;

        public UltiCommand(Combatant actor, Combatant target) : base(actor)
        {
            this.target = target;
        }

        protected override bool ValidTarget(BattleContext ctx, out string reason)
        {
            reason = null;
            if (actor.Rage < ctx.Cfg.rageMax) { reason = "Nộ chưa đầy"; return false; }
            if (target == null || target.IsAlly || !target.IsAlive) { reason = "Chọn một quái còn sống"; return false; }
            return true;
        }

        protected override void DoAction(BattleContext ctx)
        {
            actor.Rage = 0;
            ctx.Log.Add(actor.Name + " tung " + actor.CharData.ultiName + "!");
        }
    }

    // Dùng đồ: tốn lượt, trừ 1 món trong túi chung (bag[index]).
    public class ItemCommand : AllyCommand
    {
        readonly ItemData item;
        readonly int[] bag;
        readonly int index;
        readonly Combatant target;

        public ItemCommand(Combatant actor, ItemData item, int[] bag, int index, Combatant target) : base(actor)
        {
            this.item = item;
            this.bag = bag;
            this.index = index;
            this.target = target;
        }

        protected override bool ValidTarget(BattleContext ctx, out string reason)
        {
            reason = null;
            if (bag[index] <= 0) { reason = "Hết " + item.displayName; return false; }
            if (target == null || !target.IsAlive) { reason = "Chọn mục tiêu còn sống"; return false; }
            if (item.TargetsAlly != target.IsAlly) { reason = item.TargetsAlly ? "Chọn một đồng đội" : "Chọn một quái"; return false; }
            if (item.effect == ItemEffect.HealHP && target.HP >= target.MaxHP) { reason = target.Name + " đang đầy máu"; return false; }
            if (item.effect == ItemEffect.CleanseAmKhi && target.AmKhi <= 0) { reason = target.Name + " không có Âm khí"; return false; }
            return true;
        }

        string Who(Combatant t)
        {
            return t == actor ? actor.Name + " dùng " : actor.Name + " cho " + t.Name + " dùng ";
        }

        protected override void DoAction(BattleContext ctx)
        {
            bag[index]--;
            switch (item.effect)
            {
                case ItemEffect.Talisman:
                    target.HP = Mathf.Max(0, target.HP - item.power);
                    ctx.Log.Add(actor.Name + " dán " + item.displayName + " lên " + target.Name + ": -" + item.power + " HP");
                    CombatRules.RaiseFx(target, FxKind.Damage, item.power);
                    if (!target.IsAlive) ctx.Log.Add(target.Name + " gục.");
                    break;
                case ItemEffect.HealHP:
                {
                    int heal = Mathf.Min(item.power, target.MaxHP - target.HP);
                    target.HP += heal;
                    ctx.Log.Add(Who(target) + item.displayName + ": +" + heal + " HP");
                    CombatRules.RaiseFx(target, FxKind.Heal, heal);
                    break;
                }
                case ItemEffect.CleanseAmKhi:
                {
                    int cut = Mathf.Min(item.power, target.AmKhi);
                    target.AmKhi -= cut;
                    ctx.Log.Add(Who(target) + item.displayName + ": -" + cut + " Âm khí");
                    if (target.PossessedPending && target.AmKhi < ctx.Cfg.amKhiMax)
                    {
                        target.PossessedPending = false;
                        ctx.Log.Add(target.Name + " không còn bị đe dọa nhập.");
                    }
                    CombatRules.RaiseFx(target, FxKind.Cleanse, cut);
                    break;
                }
            }
        }
    }
}
