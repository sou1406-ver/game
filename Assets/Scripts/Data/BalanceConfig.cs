using UnityEngine;

namespace KyUc
{
    // Mọi con số cân bằng của combat nằm ở đây (Pillar 4: Everything Is Data).
    [CreateAssetMenu(menuName = "KyUc/Balance Config", fileName = "BalanceConfig")]
    public class BalanceConfig : ScriptableObject
    {
        [Header("Crit / Né (%)")]
        public int critCap = 80;                 // tổng crit tối đa, kể cả cộng từ thanh căng nhịp
        public float critMultiplier = 1.5f;
        public int dodgeCap = 40;
        public float luckCritPerPoint = 0.5f;    // May mắn (ẩn) cộng crit
        public float luckDodgePerPoint = 0.5f;   // May mắn (ẩn) cộng né
        public int statCap = 20;

        [Header("Đỡ")]
        [Range(0f, 1f)] public float guardReduction = 0.5f;

        [Header("Mana (skill)")]
        public int manaMax = 10;
        public int manaStart = 4;
        public int manaPerAttack = 2;   // đánh thường hồi mana
        public int skillManaCost = 4;

        [Header("Nộ (Tuyệt kỹ)")]
        public int rageMax = 100;
        public int ragePerAttack = 20;
        public int ragePerHitTaken = 10;
        public int ultiHits = 3;                 // mỗi đòn có thanh căng nhịp
        public float ultiDamageMultiplier = 1f;  // x Công mỗi đòn

        [Header("Thanh căng nhịp (chỉ trong Tuyệt kỹ)")]
        public float timingDuration = 1.0f;
        [Range(0.05f, 0.5f)] public float timingZoneWidth = 0.16f;
        public float timingZoneMin = 0.3f;
        public float timingZoneMax = 0.85f;
        public int timingMaxBonus = 40;          // bấm sát tâm
        public int timingEdgeBonus = 10;         // bấm ở mép vùng

        [Header("Gạt đòn (khi quái đánh)")]
        public float parryDuration = 0.8f;
        [Range(0.03f, 0.3f)] public float parryZoneWidth = 0.1f;
        public float parryZoneMin = 0.55f;
        public float parryZoneMax = 0.9f;
        public int ragePerParry = 10;

        [Header("Âm khí")]
        public int amKhiMax = 100;
        public int amKhiOnHit = 5;
        public int amKhiOnCrit = 10;
        public int conflictMultiplier = 2;
        public int amKhiAfterPossession = 60;

        [Header("Nhịp")]
        public float enemyActionDelay = 0.6f;
        public float turnDelay = 0.3f;

        public static BalanceConfig CreateDefault()
        {
            return CreateInstance<BalanceConfig>();
        }
    }
}
