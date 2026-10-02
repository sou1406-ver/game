using System;
using System.Collections.Generic;
using UnityEngine;

namespace KyUc
{
    [Serializable]
    public class CropDef
    {
        public string name;
        public int days;        // số ngày từ lúc trồng đến lúc chín
        public string yield;    // thu được gì
        public int yieldCount;

        public CropDef(string name, int days, string yield, int yieldCount)
        {
            this.name = name; this.days = days; this.yield = yield; this.yieldCount = yieldCount;
        }
    }

    public enum RecipeKind { Food, Offering, Combat }

    [Serializable]
    public class RecipeDef
    {
        public string output;
        public RecipeKind kind;
        public string[] needs;  // mỗi phần tử là 1 đơn vị nguyên liệu, trùng tên = cần nhiều
        public string npc;      // để trống = không cần mở khóa
        public int npcLevel;
        public int foodBonusHp; // chỉ dùng cho món ăn: +HP tối đa cả đội đêm nay

        public RecipeDef(string output, RecipeKind kind, string[] needs, string npc, int npcLevel, int foodBonusHp = 0)
        {
            this.output = output; this.kind = kind; this.needs = needs; this.npc = npc; this.npcLevel = npcLevel;
            this.foodBonusHp = foodBonusHp;
        }
    }

    [Serializable]
    public class NpcDef
    {
        public string name;
        public string role;
        public string[] levelNotes; // mức 1..5 mở ra gì

        public NpcDef(string name, string role, params string[] levelNotes)
        {
            this.name = name; this.role = role; this.levelNotes = levelNotes;
        }
    }

    [Serializable]
    public class ItemStack
    {
        public string name;
        public int count;

        public ItemStack(string name, int count)
        {
            this.name = name; this.count = count;
        }
    }

    // Toàn bộ số liệu làng ban ngày. Create → KyUc → Village Config để chỉnh.
    [CreateAssetMenu(menuName = "KyUc/Village Config", fileName = "VillageConfig")]
    public class VillageConfig : ScriptableObject
    {
        public int actionsPerDay = 4;
        public int loopDays = 30;     // hết 30 ngày thì thế giới quay lại ngày 1
        public int plotSlots = 4;     // số ô trong thửa ruộng
        public int maxAffinity = 5;   // thân thiết NPC
        public int maxBond = 5;       // gắn kết với bạn
        public int memoryCount = 10;  // số mảnh ký ức trong bản thử

        public List<CropDef> crops = new List<CropDef>();
        public List<RecipeDef> recipes = new List<RecipeDef>();
        public List<NpcDef> npcs = new List<NpcDef>();
        public List<string> friends = new List<string>();
        public List<string> ritualSet = new List<string>();  // 1 bộ lễ để sửa đình
        public List<ItemStack> startItems = new List<ItemStack>();

        public static VillageConfig CreateDefault()
        {
            var c = CreateInstance<VillageConfig>();

            // Cây: GDD mục Làng ban ngày
            c.crops.Add(new CropDef("Lúa nếp", 6, "Gạo nếp", 3));
            c.crops.Add(new CropDef("Trầu", 4, "Trầu", 2));
            c.crops.Add(new CropDef("Cau", 6, "Cau", 2));
            c.crops.Add(new CropDef("Ngải cứu", 3, "Ngải cứu", 2));
            c.crops.Add(new CropDef("Hoa huệ", 4, "Hoa huệ", 2));

            c.recipes.Add(new RecipeDef("Xôi", RecipeKind.Food, new[] { "Gạo nếp" }, "", 0, 4));
            c.recipes.Add(new RecipeDef("Mẹt gạo muối", RecipeKind.Offering, new[] { "Gạo nếp", "Muối" }, "Thầy cúng", 1));
            c.recipes.Add(new RecipeDef("Mẹt trầu cau", RecipeKind.Offering, new[] { "Trầu", "Cau" }, "Thầy cúng", 3));
            c.recipes.Add(new RecipeDef("Bó hoa huệ", RecipeKind.Offering, new[] { "Hoa huệ", "Hoa huệ" }, "Thầy cúng", 4));
            c.recipes.Add(new RecipeDef("Bùa vàng", RecipeKind.Combat, new[] { "Gạo nếp" }, "Thầy cúng", 2));
            c.recipes.Add(new RecipeDef("Thuốc hồi HP", RecipeKind.Combat, new[] { "Gạo nếp", "Muối" }, "Ông lang", 1));
            c.recipes.Add(new RecipeDef("Thuốc giảm Âm khí", RecipeKind.Combat, new[] { "Ngải cứu", "Ngải cứu" }, "Ông lang", 2));

            c.npcs.Add(new NpcDef("Thầy cúng", "Bùa, công thức đồ cúng",
                "Công thức: Mẹt gạo muối", "Công thức: Bùa vàng", "Công thức: Mẹt trầu cau", "Công thức: Bó hoa huệ", "(chưa có)"));
            c.npcs.Add(new NpcDef("Bà đồng", "Giá đồng, nghi thức nhập giá",
                "Giá đồng (chưa có trong bản này)", "(chưa có)", "(chưa có)", "(chưa có)", "(chưa có)"));
            c.npcs.Add(new NpcDef("Ông lang", "Thuốc hồi máu, giảm Âm khí",
                "Công thức: Thuốc hồi HP", "Công thức: Thuốc giảm Âm khí", "(chưa có)", "(chưa có)", "(chưa có)"));
            c.npcs.Add(new NpcDef("Cô hàng nước", "Tin đồn về luật và điểm yếu của ma",
                "Tin đồn: Ma đói nhắm người ít máu nhất, rồi người nhiều Âm khí nhất.",
                "Tin đồn: Ma nước né cao và có đòn đánh cả đội.",
                "Tin đồn: Ma nhện nhanh hơn mọi người, ra tay trước cả Vy.",
                "(chưa có)", "(chưa có)"));

            c.friends.AddRange(new[] { "Minh", "Vy", "Lan", "Tuấn", "Khoa" });
            c.ritualSet.AddRange(new[] { "Mẹt gạo muối", "Bó nhang", "Mẹt trầu cau", "Bó hoa huệ" });

            c.startItems.Add(new ItemStack("Gạo nếp", 2));
            c.startItems.Add(new ItemStack("Muối", 6));
            c.startItems.Add(new ItemStack("Bó nhang", 3));
            c.startItems.Add(new ItemStack("Bùa vàng", 1));
            c.startItems.Add(new ItemStack("Thuốc hồi HP", 1));
            return c;
        }
    }
}
