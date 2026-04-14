import ReviewCard from "../components/ReviewCard";
import ScoreCard from "../components/ScoreCard";
import Tabs from "../components/Tabs";
import { getExportPdfUrl } from "../services/api";

function formatAspectLabel(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function formatInsightText(insight) {
  if (typeof insight === "string") {
    return insight;
  }

  return insight?.text || "Insight unavailable";
}

function TagList({ items, emptyMessage, tone }) {
  if (!items.length) {
    return <p className="text-sm text-gray-500">{emptyMessage}</p>;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {items.map((item) => (
        <span
          key={item}
          className={`rounded-full px-3 py-1 text-sm font-medium ${tone}`}
        >
          {formatAspectLabel(item)}
        </span>
      ))}
    </div>
  );
}

function SwotCard({ title, items, tone, emptyMessage }) {
  return (
    <article className="rounded-2xl border border-orange-100 bg-white p-6 shadow-md transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] ${tone}`}>
          {items.length}
        </span>
      </div>
      <ul className="space-y-3 text-sm leading-6 text-gray-700">
        {items.length ? (
          items.map((item) => <li key={item}>{item}</li>)
        ) : (
          <li className="text-gray-500">{emptyMessage}</li>
        )}
      </ul>
    </article>
  );
}

function DashboardPage({
  restaurantName,
  strategyData,
  reviewFeed,
  formData,
  activeTab,
  onTabChange,
}) {
  const handleExport = () => {
    const exportUrl = getExportPdfUrl(formData);
    window.open(exportUrl, "_blank", "noopener,noreferrer");
  };

  const healthScore = strategyData?.global_score ?? 0;
  const swot = strategyData?.swot ?? {
    strengths: [],
    weaknesses: [],
    opportunities: [],
    threats: [],
  };
  const recommendations = strategyData?.recommendations ?? [];
  const fourPs = strategyData?.["4ps"] ?? {};
  const aspectScores = strategyData?.aspect_scores
    ? Object.entries(strategyData.aspect_scores)
    : [];
  const tabs = ["SWOT", "4Ps", "Insights"];

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(249,115,22,0.12),_transparent_28%),linear-gradient(180deg,_#fff7ed_0%,_#fff7ed_100%)] px-4 py-8 text-gray-800">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6">
        <section className="flex flex-col gap-4 rounded-[2rem] border border-orange-100 bg-white px-8 py-6 shadow-md lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-orange-500">
              Restaurant Intelligence Dashboard
            </p>
            <h2 className="mt-3 text-2xl font-semibold tracking-tight text-gray-800">
              {restaurantName}
            </h2>
            <p className="mt-2 text-sm leading-6 text-gray-500">
              A premium view of restaurant sentiment, strategic frameworks, and customer feedback signals.
            </p>
          </div>
          <button
            type="button"
            onClick={handleExport}
            className="inline-flex h-12 items-center justify-center rounded-xl border border-orange-200 bg-white px-5 text-sm font-semibold text-gray-700 shadow-md transition-all duration-300 hover:-translate-y-0.5 hover:bg-orange-50 hover:shadow-lg"
          >
            Export PDF
          </button>
        </section>

        <ScoreCard
          restaurantName={restaurantName}
          score={healthScore}
          summary={strategyData?.summary}
        />

        <section className="grid gap-6 lg:grid-cols-[1fr_0.95fr]">
          <article className="rounded-[2rem] border border-orange-100 bg-white p-8 shadow-md">
            <div className="grid gap-6">
              <div>
                <h2 className="text-lg font-semibold text-gray-800">Key Strengths</h2>
                <div className="mt-3">
                  <TagList
                    items={swot.strengths ?? []}
                    emptyMessage="No strengths available yet."
                    tone="bg-green-100 text-green-600"
                  />
                </div>
              </div>

              <div>
                <h2 className="text-lg font-semibold text-gray-800">Key Weaknesses</h2>
                <div className="mt-3">
                  <TagList
                    items={swot.weaknesses ?? []}
                    emptyMessage="No weaknesses available yet."
                    tone="bg-red-100 text-red-600"
                  />
                </div>
              </div>
            </div>
          </article>

          <article className="rounded-[2rem] border border-orange-100 bg-white p-8 shadow-md">
            <h2 className="text-lg font-semibold text-gray-800">Aspect Performance</h2>
            <p className="mt-2 text-sm text-gray-500">
              Most-discussed aspects are ranked first to highlight what matters most.
            </p>

            {aspectScores.length ? (
              <div className="mt-6 space-y-4">
                {aspectScores.map(([aspect, details]) => (
                  <div key={aspect} className="rounded-2xl bg-orange-50/60 p-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-semibold text-gray-800">
                        {formatAspectLabel(aspect)}
                      </h3>
                      <span className="text-sm font-semibold text-gray-500">
                        {Math.round((details.score ?? 0) * 100)}%
                      </span>
                    </div>
                    <div className="mt-3 h-2 rounded-full bg-orange-100">
                      <div
                        className="h-2 rounded-full bg-gradient-to-r from-red-500 to-orange-500"
                        style={{ width: `${Math.round((details.score ?? 0) * 100)}%` }}
                      />
                    </div>
                    <div className="mt-3 flex gap-3 text-xs font-medium text-gray-500">
                      <span className="rounded-full bg-green-100 px-3 py-1 text-green-600">
                        Positive {details.positive ?? 0}
                      </span>
                      <span className="rounded-full bg-red-100 px-3 py-1 text-red-600">
                        Negative {details.negative ?? 0}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-4 text-sm text-gray-500">No aspect data available yet.</p>
            )}
          </article>
        </section>

        <section className="rounded-[2rem] border border-orange-100 bg-white p-6 shadow-md md:p-8">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-800">Framework Explorer</h2>
              <p className="mt-2 text-sm text-gray-500">
                Switch between structured strategic views without cluttering the page.
              </p>
            </div>
            <Tabs tabs={tabs} activeTab={activeTab} onChange={onTabChange} />
          </div>

          <div className="mt-6">
            {activeTab === "SWOT" ? (
              <div className="grid gap-6 lg:grid-cols-2">
                <SwotCard
                  title="Strengths"
                  items={swot.strengths ?? []}
                  tone="bg-green-100 text-green-600"
                  emptyMessage="No strengths available."
                />
                <SwotCard
                  title="Weaknesses"
                  items={swot.weaknesses ?? []}
                  tone="bg-red-100 text-red-600"
                  emptyMessage="No weaknesses available."
                />
                <SwotCard
                  title="Opportunities"
                  items={swot.opportunities ?? []}
                  tone="bg-sky-100 text-sky-700"
                  emptyMessage="No opportunities available."
                />
                <SwotCard
                  title="Threats"
                  items={swot.threats ?? []}
                  tone="bg-amber-100 text-amber-700"
                  emptyMessage="No threats available."
                />
              </div>
            ) : null}

            {activeTab === "4Ps" ? (
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                {[
                  ["Product", fourPs.product],
                  ["Price", fourPs.price],
                  ["Place", fourPs.place],
                  ["Promotion", fourPs.promotion],
                ].map(([title, text]) => (
                  <article
                    key={title}
                    className="rounded-2xl border border-orange-100 bg-orange-50/50 p-5 shadow-md transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg"
                  >
                    <h3 className="text-sm font-semibold uppercase tracking-[0.18em] text-orange-600">
                      {title}
                    </h3>
                    <p className="mt-3 text-sm leading-7 text-gray-700">
                      {text || "Analysis will appear here after a successful request."}
                    </p>
                  </article>
                ))}
              </div>
            ) : null}

            {activeTab === "Insights" ? (
              <div className="space-y-4">
                {strategyData?.insights?.length ? (
                  strategyData.insights.map((insight) => (
                    <article
                      key={formatInsightText(insight)}
                      className="rounded-2xl border border-orange-100 bg-orange-50/50 p-5 shadow-md transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg"
                    >
                      <p className="text-sm leading-7 text-gray-700">{formatInsightText(insight)}</p>
                      {insight?.source_urls?.length ? (
                        <div className="mt-3 flex flex-wrap gap-2">
                          {insight.source_urls.map((sourceUrl) => (
                            <a
                              key={sourceUrl}
                              href={sourceUrl}
                              target="_blank"
                              rel="noreferrer"
                              className="rounded-full bg-white px-3 py-1 text-xs font-medium text-gray-700 ring-1 ring-orange-100 transition-all duration-300 hover:bg-orange-50"
                            >
                              Evidence
                            </a>
                          ))}
                        </div>
                      ) : null}
                    </article>
                  ))
                ) : (
                  <p className="text-sm text-gray-500">Insights will appear after analysis.</p>
                )}
              </div>
            ) : null}
          </div>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <article className="rounded-[2rem] border border-orange-100 bg-white p-8 shadow-md">
            <h2 className="text-xl font-semibold text-gray-800">Recommendations</h2>
            {recommendations.length ? (
              <ul className="mt-5 space-y-3 text-sm leading-7 text-gray-700">
                {recommendations.map((item) => (
                  <li key={item} className="flex gap-3 rounded-2xl bg-orange-50/60 px-4 py-3 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-md">
                    <span className="mt-1 text-orange-500">+</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-4 text-sm text-gray-500">
                Recommendations will appear after a successful analysis.
              </p>
            )}
          </article>

          <article className="rounded-[2rem] border border-orange-100 bg-white p-8 shadow-md">
            <div className="mb-5">
              <h2 className="text-xl font-semibold text-gray-800">Customer Feedback Sources</h2>
              <p className="mt-2 text-sm text-gray-500">
                A compact cross-platform feed designed to feel like a real listening surface.
              </p>
            </div>

            {reviewFeed.length ? (
              <div className="max-h-[38rem] space-y-4 overflow-y-auto pr-1">
                {reviewFeed.map((review, index) => (
                  <ReviewCard
                    key={`${review.platform}-${review.timestamp}-${index}`}
                    platform={review.platform}
                    text={review.text}
                    timestamp={review.timestamp}
                    source_url={review.source_url}
                  />
                ))}
              </div>
            ) : (
              <p className="mt-4 text-sm text-gray-500">
                Review samples will appear here after a successful analysis.
              </p>
            )}
          </article>
        </section>
      </div>
    </main>
  );
}

export default DashboardPage;
