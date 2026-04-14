function formatTimestamp(timestamp) {
  if (!timestamp) {
    return "Recently";
  }

  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) {
    return timestamp;
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
  }).format(date);
}

function buildHandle(platform, sourceUrl) {
  const fallbackPrefix = {
    google: "local-guide",
    reddit: "foodfan",
    twitter: "guest",
    zomato: "verified-diner",
  };

  const slug = sourceUrl?.split("/").filter(Boolean).pop() || "review";
  const shortSlug = slug.replace(/[^a-zA-Z0-9-]/g, "").slice(-6) || "sample";

  if (platform === "reddit") {
    return `u/${fallbackPrefix.reddit}_${shortSlug}`;
  }

  if (platform === "twitter") {
    return `@${fallbackPrefix.twitter}_${shortSlug}`;
  }

  return null;
}

function getPlatformStyles(platform) {
  if (platform === "google") {
    return {
      wrapper: "border-orange-100 bg-white",
      badge: "bg-orange-100 text-orange-700",
      accent: "text-orange-500",
    };
  }

  if (platform === "reddit") {
    return {
      wrapper: "border-slate-200 bg-slate-50",
      badge: "bg-slate-200 text-slate-700",
      accent: "text-slate-500",
    };
  }

  if (platform === "twitter") {
    return {
      wrapper: "border-orange-100 bg-white",
      badge: "bg-orange-50 text-orange-700",
      accent: "text-orange-600",
    };
  }

  return {
    wrapper: "border-red-100 bg-red-50/70",
    badge: "bg-red-100 text-red-600",
    accent: "text-red-500",
  };
}

function ReviewCard({ platform, text, timestamp, source_url }) {
  const styles = getPlatformStyles(platform);
  const handle = buildHandle(platform, source_url);

  return (
    <article className={`rounded-2xl border p-5 shadow-sm transition duration-200 hover:-translate-y-0.5 hover:shadow-md ${styles.wrapper}`}>
      <div className="flex items-start justify-between gap-3">
        <div>
          <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${styles.badge}`}>
            {platform}
          </span>
          {platform === "google" ? (
            <p className={`mt-3 text-sm font-medium ${styles.accent}`}>★ Local Review</p>
          ) : null}
          {platform === "zomato" ? (
            <p className={`mt-3 text-sm font-medium ${styles.accent}`}>4.2 Taste Score</p>
          ) : null}
          {handle ? (
            <p className={`mt-3 text-sm font-medium ${styles.accent}`}>{handle}</p>
          ) : null}
        </div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gray-400">
          {formatTimestamp(timestamp)}
        </p>
      </div>

      <p className={`mt-4 text-sm leading-7 ${platform === "twitter" ? "line-clamp-4" : ""} text-gray-800`}>
        {text}
      </p>

      {source_url ? (
        <a
          href={source_url}
          target="_blank"
          rel="noreferrer"
          className={`mt-4 inline-flex text-xs font-semibold uppercase tracking-[0.18em] ${styles.accent}`}
        >
          View source
        </a>
      ) : null}
    </article>
  );
}

export default ReviewCard;
