using System;
using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    public enum IntentType
    {
        SingleHit, // đánh 1 người
        AllHit,    // đánh cả phe
        Terrify    // dọa: cộng Âm khí cả phe
    }

    public enum TargetRule
    {
        LowestHP,
        HighestAmKhi,
        All
    }

    [Serializable]
    public class IntentDef
    {
        public string label = "Đánh";
        public IntentType type = IntentType.SingleHit;
        public int power = 5;
        public TargetRule target = TargetRule.LowestHP;

        public IntentDef() { }

        public IntentDef(string label, IntentType type, int power, TargetRule target)
        {
            this.label = label;
            this.type = type;
            this.power = power;
            this.target = target;
        }
    }

    // Quái lặp lại pattern theo thứ tự và báo trước ý định đầu mỗi vòng.
    [CreateAssetMenu(menuName = "KyUc/Enemy Data", fileName = "EnemyData")]
    public class EnemyData : ScriptableObject
    {
        public string displayName = "Ma";
        public Color color = new Color(0.3f, 0.5f, 0.95f);
        public Texture2D sprite; // để trống thì vẽ ô vuông màu
        public int maxHP = 30;
        public int defense = 0;
        [Range(0, 20)] public int crit = 0;    // %
        [Range(1, 20)] public int speed = 8;
        [Range(0, 20)] public int dodge = 0;   // % (ẩn)
        public List<IntentDef> pattern = new List<IntentDef>();

        public static EnemyData Create(string name, Color color, int hp, int def, int crit, int speed, int dodge,
            params IntentDef[] pattern)
        {
            var d = CreateInstance<EnemyData>();
            d.displayName = name;
            d.color = color;
            d.maxHP = hp;
            d.defense = def;
            d.crit = crit;
            d.speed = speed;
            d.dodge = dodge;
            d.pattern = new List<IntentDef>(pattern);
            return d;
        }
    }
}
