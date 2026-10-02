using System;
using UnityEngine;

namespace KyUc
{
    // Một địa điểm trên map. x y w h: khung sprite; dx dy: chỗ đứng trước cửa để bấm E. Đơn vị: pixel map.
    // kind: home (nấu ăn, làm đồ) · field (ruộng) · dinh (sửa đình) · npc (thăm người) · shrine (đi đêm) · locked (điện chưa mở)
    [Serializable]
    public class MapSpot
    {
        public string id, name, kind, npc;
        public int x, y, w, h, dx, dy;
    }

    [Serializable]
    public class MapRect
    {
        public int x, y, w, h;
    }

    [Serializable]
    public class MapFriend
    {
        public string name;
        public int x, y;
    }

    // Nhà, cây, đồ vật: ô (ax, ay, w, h) trong atlas, đặt tại (x, y) trên map, vẽ theo đáy b cùng người chơi.
    [Serializable]
    public class MapObject
    {
        public int ax, ay, w, h, x, y, b;
        public bool fade; // người chơi đi ra sau thì làm mờ
    }

    // Map làng do ArtSource/draw_world.py sinh ra trong Assets/Resources/World/.
    [Serializable]
    public class VillageMap
    {
        public int width = 960, height = 640, cell = 4, cols, rows;
        public string solid = "";                   // lưới va chạm, '1' = không đi qua được
        public MapSpot[] spots = new MapSpot[0];
        public MapRect[] plots = new MapRect[0];    // các ô ruộng, khớp với VillageState.Plots theo thứ tự
        public MapRect[] smoke = new MapRect[0];    // chỗ khói bếp (chỉ dùng x, y)
        public MapFriend[] friends = new MapFriend[0];
        public MapRect spawn = new MapRect();       // chỗ thức dậy mỗi sáng
        public MapObject[] objects = new MapObject[0];
        [NonSerialized] public Texture2D ground, atlas;

        public bool Loaded
        {
            get { return spots.Length > 0 && ground != null; }
        }

        public bool Solid(float x, float y)
        {
            if (x < 0 || y < 0 || x >= width || y >= height) return true;
            int gx = (int)(x / cell), gy = (int)(y / cell);
            int i = gy * cols + gx;
            return i >= 0 && i < solid.Length && solid[i] == '1';
        }

        public static VillageMap Load()
        {
            var json = Resources.Load<TextAsset>("World/world");
            var m = json != null ? JsonUtility.FromJson<VillageMap>(json.text) : new VillageMap();
            m.ground = PixelTex.Load("World/ground");
            m.atlas = PixelTex.Load("World/objects");
            if (!m.Loaded) Debug.LogWarning("Thiếu Resources/World. Chạy ArtSource/draw_world.py.");
            return m;
        }
    }
}
