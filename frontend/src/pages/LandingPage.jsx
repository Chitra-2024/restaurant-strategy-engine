import RestaurantForm from "../components/RestaurantForm";

function LandingPage({ formData, onChange, onSubmit, isLoading, error }) {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(239,68,68,0.12),_transparent_30%),linear-gradient(180deg,_#fff7ed_0%,_#fff7ed_100%)] px-4 py-10 text-gray-800">
      <div className="mx-auto flex min-h-[calc(100vh-5rem)] max-w-6xl flex-col justify-center gap-12">
        <section className="mx-auto max-w-3xl text-center">
          <div className="inline-flex rounded-full border border-orange-200 bg-white px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-orange-600 shadow-md">
            Strategic Intelligence Platform
          </div>
          <h1 className="mt-8 text-5xl font-semibold tracking-tight text-gray-800 md:text-7xl">
            Restaurant Strategy Engine
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-gray-500">
            Transform customer feedback into actionable business insights
          </p>
        </section>

        <section className="mx-auto w-full max-w-4xl rounded-[2rem] border border-orange-100 bg-white p-6 shadow-md backdrop-blur md:p-8">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-800">Start an Analysis</h2>
            <p className="mt-2 text-sm leading-6 text-gray-500">
              Enter a restaurant, optionally narrow the location and date window, and generate a full strategic dashboard.
            </p>
          </div>

          <RestaurantForm
            formData={formData}
            onChange={onChange}
            onSubmit={onSubmit}
            isLoading={isLoading}
            submitLabel="Analyze"
          />

          {error ? (
            <div className="mt-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
              {error}
            </div>
          ) : null}
        </section>
      </div>
    </main>
  );
}

export default LandingPage;
