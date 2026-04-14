function getScoreTone(score) {
  if (score > 70) {
    return {
      value: "bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent",
      badge: "bg-emerald-100 text-emerald-700",
      label: "Strong",
    };
  }

  if (score >= 40) {
    return {
      value: "bg-gradient-to-r from-orange-500 to-amber-400 bg-clip-text text-transparent",
      badge: "bg-orange-100 text-orange-700",
      label: "Moderate",
    };
  }

  return {
    value: "bg-gradient-to-r from-red-600 to-orange-500 bg-clip-text text-transparent",
    badge: "bg-rose-100 text-rose-700",
    label: "Needs Attention",
  };
}

function ScoreCard({ restaurantName, score, summary }) {
  const tone = getScoreTone(score);

  return (
    <section className="rounded-[2rem] border border-orange-100 bg-white px-8 py-10 shadow-md">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gray-500">
            Restaurant Overview
          </p>
          <h1 className="mt-4 text-3xl font-semibold tracking-tight text-gray-800 md:text-5xl">
            {restaurantName || "Restaurant Strategy Dashboard"}
          </h1>
          <p className="mt-4 text-base leading-7 text-gray-500">
            {summary || "Run an analysis to generate a strategic overview."}
          </p>
        </div>

        <div className="min-w-[220px] rounded-[1.75rem] border border-red-100 bg-gradient-to-br from-red-50 via-white to-orange-50 px-6 py-6 text-gray-800 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gray-500">
            Global Score
          </p>
          <div className="mt-3 flex items-end gap-3">
            <span className={`text-6xl font-semibold tracking-tight ${tone.value}`}>
              {score}
            </span>
            <span className={`mb-2 rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${tone.badge}`}>
              {tone.label}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ScoreCard;
