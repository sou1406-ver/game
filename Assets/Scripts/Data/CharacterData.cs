using UnityEngine;

namespace KyUc
{
    public enum SkillType
    {
        PowerStrike,   // đòn mạnh vào 1 quái
        CancelIntent,  // hủy ý định đã báo của 1 quái
        Shield         // khiên cho 1 đồng đội
    }

    [CreateAssetMenu(menuName = "KyUc/Character Data", fileName = "CharacterData")]
    public class CharacterData : ScriptableObject
    {
        public string displayName = "Nhân vật";
        public string role = "";   // vai trong trận, hiện trên thẻ (GDD mục Nhân vật), ví dụ "Kiểm soát · Phá đòn"
        public Color color = new Color(0.85f, 0.25f, 0.25f);
        public Texture2D sprite;   // để trống thì vẽ ô vuông màu
        public Texture2D portrait; // chân dung 48x48 cạnh menu lệnh, sau này dùng cho hội thoại

        [Header("Chỉ số hiện")]
        public int maxHP = 24;
        public int attack = 5;
        public int defense = 2;
        [Range(0, 20)] public int crit = 5;    // %
        [Range(1, 20)] public int speed = 10;  // ai nhanh đi trước
        [Range(0f, 0.5f)] public float amKhiResist = 0f;
        public bool hasConflict = true;        // khúc mắc chưa giải: nhận gấp đôi Âm khí

        [Header("Chỉ số ẩn")]
        [Range(0, 20)] public int dodge = 5;   // %
        [Range(0, 10)] public int luck = 2;

        [Header("Skill (tốn mana)")]
        public string skillName = "Skill";
        public SkillType skillType = SkillType.PowerStrike;
        public float skillPower = 2f;

        [Header("Tuyệt kỹ (Nộ đầy)")]
        public string ultiName = "Tuyệt kỹ";

        public bool SkillTargetsAlly
        {
            get { return skillType == SkillType.Shield; }
        }

        public static CharacterData Create(string name, Color color, int hp, int atk, int def, int crit, int speed,
            int dodge, int luck, float resist, string skillName, SkillType skill, float power, string role = "")
        {
            var d = CreateInstance<CharacterData>();
            d.displayName = name;
            d.role = role;
            d.color = color;
            d.maxHP = hp;
            d.attack = atk;
            d.defense = def;
            d.crit = crit;
            d.speed = speed;
            d.dodge = dodge;
            d.luck = luck;
            d.amKhiResist = resist;
            d.skillName = skillName;
            d.skillType = skill;
            d.skillPower = power;
            return d;
        }
    }
}
