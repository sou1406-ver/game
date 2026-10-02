using UnityEngine;

namespace KyUc
{
    public enum ItemEffect
    {
        Talisman,     // bùa: sát thương thẳng lên quái, bỏ qua Thủ và né
        HealHP,       // hồi HP cho đồng đội
        CleanseAmKhi  // giảm Âm khí, gỡ trạng thái "sắp bị nhập"
    }

    // Đồ dùng trong trận. Dùng đồ tốn lượt của người dùng; túi đồ dùng chung cả đội.
    [CreateAssetMenu(menuName = "KyUc/Item Data", fileName = "ItemData")]
    public class ItemData : ScriptableObject
    {
        public string displayName = "Đồ";
        public Texture2D icon;
        public ItemEffect effect = ItemEffect.HealHP;
        public int power = 10;
        public int startCount = 2; // số lượng mang vào mỗi trận

        public bool TargetsAlly
        {
            get { return effect != ItemEffect.Talisman; }
        }

        public string Description
        {
            get
            {
                switch (effect)
                {
                    case ItemEffect.Talisman: return "Dán lên 1 quái: " + power + " sát thương, bỏ qua Thủ và né.";
                    case ItemEffect.HealHP: return "Hồi " + power + " HP cho 1 đồng đội.";
                    default: return "Giảm " + power + " Âm khí cho 1 đồng đội, gỡ \"sắp bị nhập\" nếu xuống dưới mức đầy.";
                }
            }
        }

        public static ItemData Create(string name, ItemEffect effect, int power, int count)
        {
            var d = CreateInstance<ItemData>();
            d.displayName = name;
            d.effect = effect;
            d.power = power;
            d.startCount = count;
            return d;
        }
    }
}
