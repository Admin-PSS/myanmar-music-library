import { useState, useMemo } from "react";

const albums = [
  {
    id: 1,
    artist: "မာမာအေး",
    title: "ဓါတ်ပြားတေး အမှတ် (၃)",
    year: null,
    type: "ဓါတ်ပြားတေး",
    format: "MP3 / 320 KBPS / 125 MB",
    recordLabel: "ဟိုင်းဖိုင် တေးသံသွင်း (ရန်ကုန်)",
    coverUrl: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVxavDN9d_YmvPdS-ejzgOZWn9XT_K_wFECJYbuO0kfdtIQCipeD7qQdrAmmcGu85Tgoz0vidtvqBi6c2LijXACzJ8RhEQeMUcbvawH7suwykvfYiXj15uF4b-nhT3yy8LUuj0vPBbwyLOfaKdqHf4DTbi5bg0k5t7pvwWwkbkhwHefqUFvfZetGA085Q/w400-h374/MMA%20C%20ART-3.jpg",
    blogUrl: "https://phyuniwarpyar.blogspot.com/2026/06/blog-post_572.html",
    pcloudUrl: "https://u.pcloud.link/publink/show?code=kZyr4N5ZjsPINsFHxomL721wcNsuFXR6Uyzk",
    mediafire: "https://www.mediafire.com/folder/ttj702kyd5xfx/2026+UP(62)",
    tracklist: [
      "ရွှေလမှာဆုံကြမယ်",
      "အောင်မြေမြမန်း",
      "သခင်လိုလို လင်လိုလို",
      "ပန်ချင်သူ ပျို့ချစ်ဦးရယ်",
      "မောင့်ရင်ထဲမှာ နေတစ်ရာ နွေတစ်ရာ",
      "ပျို့ဆုတောင်း",
      "ချစ်ရေစင်",
      "စန္ဒကိန္နရီ",
      "ရေမြေဆုံးစေတော့",
      "မျှမျှတတချစ်ကြပါ",
      "ခုနှစ်ထွေမင်းသား",
      "မာန်",
    ],
  },
  {
    id: 2,
    artist: "ဖိုးရှမ်း",
    title: "နေမင်းထဲကလူ",
    year: "၁၉၈၀",
    type: "တိတ်ခွေ",
    format: "MP3 / 192 KBPS / 146 MB",
    recordLabel: "Success • မေ စတူဒီယို",
    coverUrl: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjhBSbjQO9tNEUNrMvhIlTaqn3C1IKmbB3lM_Ncpndc9emS0Spf1_8LKD8EOqhxX5Ko4jsMjtw8QRBD4VHi-tuIS7XEw4mVmnS5RUElP6r_oGv0YJbKU1llXjoSR7bMzfWRmHxyNr9RYJhXaQgpuUAGSsDcLnrpkp2lhrmIcOVC6lXgp4zuW3_9ldYUqIQ/w400-h384/20.Tape%20Cover.jpg",
    blogUrl: "https://phyuniwarpyar.blogspot.com/2026/06/blog-post_22.html",
    pcloudUrl: "https://u.pcloud.link/publink/show?code=kZj34N5Z0YOkjnM1LruvtfSMO9O4F8TDUBBy",
    mediafire: "https://www.mediafire.com/folder/67v28ntnlc4ze/2026+UP(63)",
    tracklist: [
      "လိမ့်နေသောကျောက်ခဲလေးများ",
      "လူဆိုးလေးလို့ထင်မှာစိုးတယ်",
      "ငပလီသွားမယ် အချစ်လိုက်ခဲ့",
      "အချစ်ဆုံးရဲ့နောက်ဆုံးနေ့များ",
      "အချစ်ဦးတွက်အမုန်းမရှိပါ",
      "ဓူဝံကြယ်လေးကူညီပေးပါ",
      "နေမင်းထဲကလူ",
      "စက်ဘီးလေးမြင်တိုင်းလွမ်းတယ်",
      "နွေမိုးဆောင်းရဲ့အလွမ်းသမား",
      "ပြန်မလာနဲ့တော့",
      "ညှာတာပါမိုး",
      "မီးရောင်ကိုရွှေတောင်ထင်မိပါ၍",
      "အထီးကျန်ကျနော်",
      "ချစ်တိုင်းမညားလူတန်းစားပြဿနာ",
      "ကျောင်းသွားကြစို့",
      "သန်းခေါင်ယံညရဲ့သီချင်းသည်",
      "ရေခပ်လမ်း",
      "အခန်အောင်းပြီးဆွေးနေသည်",
      "အသဲရိုင်းတွက်စီရင်ချက်",
    ],
  },
  {
    id: 3,
    artist: "ဟင်္သာတထွန်းရင်",
    title: "နွေမာယာရှင်",
    year: "၁၉၉၆",
    type: "တိတ်ခွေ",
    format: "Cover Only (Audio မရှိသေး)",
    recordLabel: "G-SEVEN • MAY STUDIO",
    coverUrl: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi1F7exOM3eyurme3t65b6dT9sF8lK0TOIMNA9W4gh4U42wu61klMkpWK3jR8HVW_aQ7kFi1XXWtbUvtD8OD250OnbudmtNV4K0e1KIokVsaQM0wbtDC6d0E9ng7jJCy6vUPW1b0Iww9eN7xh0UTW7lABP44XEYLrGm5H-xn8nLKNJRBg0fYuKH3id47Eo/w400-h385/Nwe%20Maryar%20Shin.jpg",
    blogUrl: "https://phyuniwarpyar.blogspot.com/2026/06/cover-only.html",
    pcloudUrl: null,
    mediafire: null,
    tracklist: [
      "အညာနွေပန်းချီကား",
      "နွေမာယာရှင်",
      "ရူးပြီဗျို့",
      "ပုတ်သင်ညို",
      "အိုးပုတ်ချိုးရုပ်",
      "အကယ်ဒမီညိုမြ",
      "အသဲဖျက်မလေးမိမာယာ",
      "အပယ်ခံမလေး",
      "လက်ညှိုးညွှန်ရာ",
      "မင်းနန္ဒာလိုအချစ်မျိုး",
    ],
  },
  {
    id: 4,
    artist: "ထူးသာ၊ ငြိမ်းငြိမ်းအိ၊ ဂျော်လီဆွေ",
    title: "အချစ်မှာ ဇရာမရှိ",
    year: null,
    type: "ကက်ဆက်ဇာတ်လမ်း",
    format: "MP3 / 128 KBPS / 54 MB",
    recordLabel: "နန်းအမရ (ဒါရိုက်တာ မောင်မောင်သိန်း)",
    coverUrl: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjUodBzaEjz3WuyRnvJlFvqZN4_a3mCsd8cxLXvNgUxvMDQKDT6Xbt_27ofW1bT3BGpkFi6zIgApEXWX0WRN9isvzhyphenhyphenz0DR7nvqzcV82ojgwoUgTRVh-IpNXbseWUU0AHGva6v-0mHRtd3Tp2W827C8t8n9P2E711sQHorPfEDrNL2zHD8ChcY0P21vTMc/w400-h384/02.Tape%20Cover.jpg",
    blogUrl: "https://phyuniwarpyar.blogspot.com/2026/06/blog-post_751.html",
    pcloudUrl: "https://u.pcloud.link/publink/show?code=kZIf4N5Z6y8lSY37Bn8t1Qz6zEsh45vYVr3k",
    mediafire: "https://www.mediafire.com/file/0b7lgykgsdg5req/01.mp3/file",
    tracklist: ["အချစ်မှာ ဇရာမရှိ ဇာတ်လမ်း (တစ်ပုဒ်တည်း)"],
  },
];

const TYPE_COLORS = {
  "ဓါတ်ပြားတေး": { bg: "#fef3c7", text: "#92400e", dot: "#f59e0b" },
  "တိတ်ခွေ": { bg: "#dbeafe", text: "#1e40af", dot: "#3b82f6" },
  "ကက်ဆက်ဇာတ်လမ်း": { bg: "#fce7f3", text: "#9d174d", dot: "#ec4899" },
};

function Badge({ type }) {
  const c = TYPE_COLORS[type] || { bg: "#f3f4f6", text: "#374151", dot: "#6b7280" };
  return (
    <span style={{ background: c.bg, color: c.text, fontSize: 11, fontWeight: 600, padding: "2px 8px", borderRadius: 99, display: "inline-flex", alignItems: "center", gap: 4 }}>
      <span style={{ width: 6, height: 6, borderRadius: "50%", background: c.dot, display: "inline-block" }} />
      {type}
    </span>
  );
}

function AlbumCard({ album, onClick, isSelected }) {
  const hasAudio = album.pcloudUrl || album.mediafire;
  return (
    <div
      onClick={() => onClick(album)}
      style={{
        background: isSelected ? "#1e1b4b" : "#ffffff",
        border: isSelected ? "2px solid #7c3aed" : "2px solid #f1f0ff",
        borderRadius: 16,
        padding: 16,
        cursor: "pointer",
        transition: "all 0.18s ease",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* cover art */}
      <div style={{ position: "relative", marginBottom: 12 }}>
        <img
          src={album.coverUrl}
          alt={album.title}
          style={{ width: "100%", aspectRatio: "1/1", objectFit: "cover", borderRadius: 10, display: "block" }}
          onError={(e) => { e.target.style.display = "none"; }}
        />
        {!hasAudio && (
          <div style={{ position: "absolute", top: 8, right: 8, background: "#374151", color: "#fff", fontSize: 10, fontWeight: 700, padding: "2px 6px", borderRadius: 6 }}>
            NO AUDIO
          </div>
        )}
      </div>

      <Badge type={album.type} />
      <div style={{ marginTop: 8, fontWeight: 700, fontSize: 13, color: isSelected ? "#e0e7ff" : "#1e1b4b", lineHeight: 1.4, fontFamily: "'Padauk', sans-serif" }}>
        {album.title}
      </div>
      <div style={{ fontSize: 12, color: isSelected ? "#a5b4fc" : "#7c3aed", fontWeight: 600, marginTop: 2 }}>
        {album.artist}
      </div>
      {album.year && (
        <div style={{ fontSize: 11, color: isSelected ? "#818cf8" : "#9ca3af", marginTop: 2 }}>
          {album.year}
        </div>
      )}
    </div>
  );
}

function DetailPanel({ album, onClose }) {
  if (!album) return null;
  const hasAudio = album.pcloudUrl || album.mediafire;

  return (
    <div style={{ background: "#fafaf9", borderRadius: 20, padding: 24, height: "100%", overflowY: "auto", boxSizing: "border-box" }}>
      {/* header */}
      <div style={{ display: "flex", gap: 16, marginBottom: 20 }}>
        <img
          src={album.coverUrl}
          alt={album.title}
          style={{ width: 100, height: 100, objectFit: "cover", borderRadius: 12, flexShrink: 0, boxShadow: "0 4px 16px rgba(124,58,237,0.15)" }}
          onError={(e) => { e.target.style.display = "none"; }}
        />
        <div>
          <Badge type={album.type} />
          <div style={{ fontWeight: 800, fontSize: 17, color: "#1e1b4b", marginTop: 6, lineHeight: 1.3, fontFamily: "'Padauk', sans-serif" }}>
            {album.title}
          </div>
          <div style={{ fontSize: 14, color: "#7c3aed", fontWeight: 700, marginTop: 2 }}>{album.artist}</div>
          {album.year && <div style={{ fontSize: 12, color: "#9ca3af", marginTop: 2 }}>{album.year}</div>}
          <div style={{ fontSize: 11, color: "#6b7280", marginTop: 4 }}>{album.recordLabel}</div>
        </div>
      </div>

      {/* format */}
      <div style={{ background: "#ede9fe", borderRadius: 10, padding: "8px 12px", marginBottom: 16, fontSize: 12, color: "#4c1d95", fontWeight: 600 }}>
        📁 {album.format}
      </div>

      {/* download links */}
      {hasAudio && (
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#9ca3af", letterSpacing: "0.08em", marginBottom: 8, textTransform: "uppercase" }}>
            Download Links
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {album.pcloudUrl && (
              <a href={album.pcloudUrl} target="_blank" rel="noopener noreferrer"
                style={{ display: "flex", alignItems: "center", gap: 8, background: "#7c3aed", color: "#fff", padding: "10px 14px", borderRadius: 10, textDecoration: "none", fontSize: 13, fontWeight: 600 }}>
                ☁️ pCloud Download
              </a>
            )}
            {album.mediafire && (
              <a href={album.mediafire} target="_blank" rel="noopener noreferrer"
                style={{ display: "flex", alignItems: "center", gap: 8, background: "#1d4ed8", color: "#fff", padding: "10px 14px", borderRadius: 10, textDecoration: "none", fontSize: 13, fontWeight: 600 }}>
                🔵 MediaFire Download
              </a>
            )}
            <a href={album.blogUrl} target="_blank" rel="noopener noreferrer"
              style={{ display: "flex", alignItems: "center", gap: 8, background: "#f3f4f6", color: "#374151", padding: "10px 14px", borderRadius: 10, textDecoration: "none", fontSize: 13, fontWeight: 600 }}>
              🔗 Blog Post
            </a>
          </div>
        </div>
      )}
      {!hasAudio && (
        <div style={{ marginBottom: 20 }}>
          <a href={album.blogUrl} target="_blank" rel="noopener noreferrer"
            style={{ display: "flex", alignItems: "center", gap: 8, background: "#f3f4f6", color: "#374151", padding: "10px 14px", borderRadius: 10, textDecoration: "none", fontSize: 13, fontWeight: 600 }}>
            🔗 Blog Post
          </a>
        </div>
      )}

      {/* tracklist */}
      <div>
        <div style={{ fontSize: 11, fontWeight: 700, color: "#9ca3af", letterSpacing: "0.08em", marginBottom: 10, textTransform: "uppercase" }}>
          Tracklist — {album.tracklist.length} tracks
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
          {album.tracklist.map((track, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 10px", borderRadius: 8, background: i % 2 === 0 ? "#f5f3ff" : "transparent" }}>
              <span style={{ fontSize: 11, color: "#a78bfa", fontWeight: 700, minWidth: 20, textAlign: "right" }}>
                {String(i + 1).padStart(2, "0")}
              </span>
              <span style={{ fontSize: 13, color: "#1e1b4b", fontFamily: "'Padauk', sans-serif" }}>{track}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [selected, setSelected] = useState(albums[0]);
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("All");

  const types = ["All", ...Array.from(new Set(albums.map((a) => a.type)))];

  const filtered = useMemo(() => {
    return albums.filter((a) => {
      const matchType = filterType === "All" || a.type === filterType;
      const q = search.toLowerCase();
      const matchSearch =
        !q ||
        a.artist.includes(q) ||
        a.title.includes(q) ||
        a.tracklist.some((t) => t.includes(q));
      return matchType && matchSearch;
    });
  }, [search, filterType]);

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg, #ede9fe 0%, #f5f3ff 50%, #dbeafe 100%)", fontFamily: "'Padauk', 'Segoe UI', sans-serif" }}>
      {/* Google Font */}
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Padauk:wght@400;700&display=swap');`}</style>

      {/* Header */}
      <div style={{ background: "rgba(255,255,255,0.85)", backdropFilter: "blur(12px)", borderBottom: "1px solid #ede9fe", padding: "16px 24px", position: "sticky", top: 0, zIndex: 10 }}>
        <div style={{ maxWidth: 1100, margin: "0 auto" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
            <div style={{ width: 36, height: 36, background: "linear-gradient(135deg,#7c3aed,#3b82f6)", borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18 }}>
              🎵
            </div>
            <div>
              <div style={{ fontWeight: 800, fontSize: 16, color: "#1e1b4b" }}>ဖြူနီဝါပြာ Music Library</div>
              <div style={{ fontSize: 11, color: "#7c3aed" }}>မြန်မာ့ရှေးဟောင်း တေးသံသာများ</div>
            </div>
          </div>

          {/* Search + filters */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Artist, album, or song name ..."
              style={{ flex: 1, minWidth: 180, padding: "8px 14px", borderRadius: 10, border: "1.5px solid #ddd6fe", fontSize: 13, outline: "none", fontFamily: "inherit" }}
            />
            {types.map((t) => (
              <button
                key={t}
                onClick={() => setFilterType(t)}
                style={{
                  padding: "8px 14px", borderRadius: 10, border: "1.5px solid",
                  borderColor: filterType === t ? "#7c3aed" : "#e5e7eb",
                  background: filterType === t ? "#7c3aed" : "#fff",
                  color: filterType === t ? "#fff" : "#374151",
                  fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit"
                }}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Body */}
      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "20px 16px", display: "grid", gridTemplateColumns: "1fr 360px", gap: 20, alignItems: "start" }}>
        {/* Grid */}
        <div>
          <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 12 }}>
            {filtered.length} album{filtered.length !== 1 ? "s" : ""} found
          </div>
          {filtered.length === 0 ? (
            <div style={{ textAlign: "center", padding: 48, color: "#9ca3af", fontSize: 14 }}>
              No albums match your search.
            </div>
          ) : (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 14 }}>
              {filtered.map((a) => (
                <AlbumCard key={a.id} album={a} onClick={setSelected} isSelected={selected?.id === a.id} />
              ))}
            </div>
          )}
        </div>

        {/* Detail Panel */}
        <div style={{ position: "sticky", top: 120 }}>
          {selected ? (
            <DetailPanel album={selected} onClose={() => setSelected(null)} />
          ) : (
            <div style={{ textAlign: "center", padding: 40, color: "#9ca3af", fontSize: 14 }}>
              Select an album to view details
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div style={{ textAlign: "center", padding: "16px", fontSize: 11, color: "#a78bfa" }}>
        Source: <a href="https://phyuniwarpyar.blogspot.com" target="_blank" rel="noopener noreferrer" style={{ color: "#7c3aed" }}>phyuniwarpyar.blogspot.com</a> · မူပိုင်ခွင့်များကို လေးစားပါသည်
      </div>
    </div>
  );
}
