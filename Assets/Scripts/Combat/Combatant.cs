using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    // Trạng thái runtime của một nhân vật hoặc một quái trong trận.
    public class Combatant
    {
        public string Name;
        public Color Color;
        public bool IsAlly;

        public int MaxHP, HP, Attack, Defense, Crit, Speed;
        public int Dodge, Luck; // ẩn
        public float AmKhiResist;
        public bool HasConflict;

        public int AmKhi, Shield, Mana, Rage;
        public bool Guarding;

        // Bị nhập: đầy Âm khí thì đến lượt mình sẽ đánh đồng đội.
        public bool PossessedPending, Possessed;
        public Combatant PossessionTarget;

        public CharacterData CharData;
        public EnemyData EnemyData;

        // Ý định của quái
        public int PatternIndex;
        public IntentDef Intent;
        public readonly List<Combatant> IntentTargets = new List<Combatant>();
        public bool IntentCanceled;

        public bool IsAlive
        {
            get { return HP > 0; }
        }

        public static Combatant FromCharacter(CharacterData d, BalanceConfig cfg)
        {
            return new Combatant
            {
                Name = d.displayName,
                Color = d.color,
                IsAlly = true,
                MaxHP = d.maxHP,
                HP = d.maxHP,
                Attack = d.attack,
                Defense = d.defense,
                Crit = Mathf.Min(d.crit, cfg.statCap),
                Speed = d.speed,
                Dodge = Mathf.Min(d.dodge, cfg.statCap),
                Luck = d.luck,
                AmKhiResist = d.amKhiResist,
                HasConflict = d.hasConflict,
                Mana = cfg.manaStart,
                CharData = d
            };
        }

        public static Combatant FromEnemy(EnemyData d, BalanceConfig cfg)
        {
            return new Combatant
            {
                Name = d.displayName,
                Color = d.color,
                IsAlly = false,
                MaxHP = d.maxHP,
                HP = d.maxHP,
                Defense = d.defense,
                Crit = Mathf.Min(d.crit, cfg.statCap),
                Speed = d.speed,
                Dodge = Mathf.Min(d.dodge, cfg.statCap),
                EnemyData = d
            };
        }
    }
}
