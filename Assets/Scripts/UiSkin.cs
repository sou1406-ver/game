using UnityEngine;

namespace KyUc
{
    // Nạp ảnh pixel art từ Resources và ép lọc Point (phòng khi ảnh bị nhập với Bilinear, hình sẽ mờ).
    public static class PixelTex
    {
        public static Texture2D Load(string path)
        {
            var t = Resources.Load<Texture2D>(path);
            if (t != null)
            {
                t.filterMode = FilterMode.Point;
                t.wrapMode = TextureWrapMode.Clamp;
            }
            return t;
        }
    }

    // Khung giao diện pixel dùng chung cho làng và trận. Ảnh: Assets/Resources/UI/ (sinh bằng ArtSource/draw_ui.py).
    // Thiếu ảnh thì style tương ứng là null (riêng nút thì về nút mặc định của Unity).
    public static class UiSkin
    {
        public static readonly Color Cream = new Color(0.93f, 0.89f, 0.77f);
        public static readonly Color Gold = new Color(1f, 0.85f, 0.3f);

        public static void Build(System.Func<string, Texture2D> tex,
            out GUIStyle panel, out GUIStyle btn, out GUIStyle tabOn, out GUIStyle plaque, out GUIStyle tip)
        {
            btn = new GUIStyle(GUI.skin.button) { fontSize = 15, fontStyle = FontStyle.Bold, wordWrap = false };
            var bg = tex("UI/button");
            if (bg != null)
            {
                btn.normal.background = bg;
                btn.hover.background = tex("UI/button_hover");
                btn.active.background = tex("UI/button_down");
                btn.focused.background = bg;
                btn.border = new RectOffset(8, 8, 8, 8);
                btn.padding = new RectOffset(10, 10, 4, 6);
            }
            btn.normal.textColor = btn.focused.textColor = Cream;
            btn.hover.textColor = new Color(1f, 0.95f, 0.8f);
            btn.active.textColor = Gold;

            tabOn = new GUIStyle(btn);
            tabOn.normal.background = tabOn.hover.background = btn.active.background;
            tabOn.normal.textColor = tabOn.hover.textColor = Gold;

            panel = Make(tex("UI/panel"), 10);
            plaque = Make(tex("UI/plaque"), 6);
            tip = Make(tex("UI/tip"), 6);
        }

        static GUIStyle Make(Texture2D t, int border)
        {
            if (t == null) return null;
            return new GUIStyle { normal = { background = t }, border = new RectOffset(border, border, border, border) };
        }
    }
}
