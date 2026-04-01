function HealthCheckCard({ onCheck, response, isLoading, error }) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Backend Connection</h2>
          <p className="text-sm text-slate-600">
            Use the health endpoint to confirm frontend and backend communication.
          </p>
        </div>

        <button
          type="button"
          onClick={onCheck}
          disabled={isLoading}
          className="inline-flex items-center justify-center rounded-lg bg-brand-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-900 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? "Checking..." : "Check API Health"}
        </button>
      </div>

      <div className="mt-4 rounded-xl bg-slate-50 p-4 text-sm text-slate-700">
        {error && <p className="text-red-600">{error}</p>}
        {!error && response && <p>Response: {response.status}</p>}
        {!error && !response && <p>No request sent yet.</p>}
      </div>
    </section>
  );
}

export default HealthCheckCard;

