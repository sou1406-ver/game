using UnityEditor;

namespace KyUc.EditorTools
{
    // Tự đặt chế độ pixel nét (Point, không nén, không mipmap, giữ kích thước) cho ảnh trong các thư mục pixel art.
    public class PixelArtImporter : AssetPostprocessor
    {
        static readonly string[] Dirs = { "/Characters/", "/Enemies/", "/Items/", "/Portraits/", "/UI/", "/World/", "/Walk/", "/Battle/" };

        // Tăng số này khi đổi cài đặt bên dưới: Unity sẽ tự nhập lại toàn bộ ảnh.
        public override uint GetVersion()
        {
            return 3;
        }

        void OnPreprocessTexture()
        {
            if (!System.Array.Exists(Dirs, d => assetPath.Contains(d))) return;
            var importer = (TextureImporter)assetImporter;
            importer.npotScale = TextureImporterNPOTScale.None; // giữ nguyên kích thước ảnh, không kéo về luỹ thừa của 2
            importer.maxTextureSize = 2048;
            importer.filterMode = UnityEngine.FilterMode.Point;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.mipmapEnabled = false;
            importer.alphaIsTransparency = true;
        }
    }
}
