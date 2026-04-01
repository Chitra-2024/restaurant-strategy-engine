import { useState } from "react";

import HealthCheckCard from "../components/HealthCheckCard";
import RestaurantForm from "../components/RestaurantForm";
import { fetchHealthStatus } from "../services/api";

const initialFormData = {
  restaurantName: "",
  location: "",
  dateRange: "",
  zomatoUrl: "",
};

function DashboardPage() {
  const [formData, setFormData] = useState(initialFormData);
  const [healthResponse, setHealthResponse] = useState(null);
  const [isChecking, setIsChecking] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleHealthCheck = async () => {
    setIsChecking(true);
    setError("");

    try {
      const response = await fetchHealthStatus();
      setHealthResponse(response);
    } catch (requestError) {
      setError(requestError.message || "Unable to reach backend.");
      setHealthResponse(null);
    } finally {
      setIsChecking(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-100 via-white to-brand-50 px-4 py-10">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
        <section className="rounded-3xl bg-slate-900 px-8 py-10 text-white shadow-xl">
          <p className="text-sm uppercase tracking-[0.2em] text-brand-100">Phase 1</p>
          <h1 className="mt-3 text-3xl font-bold">Restaurant Strategy Engine</h1>
          <p className="mt-3 max-w-2xl text-sm text-slate-300">
            Base project setup for collecting restaurant inputs and validating backend connectivity.
          </p>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-slate-900">Restaurant Input Form</h2>
            <p className="text-sm text-slate-600">
              These fields prepare the UI for later scraping and analytics phases without adding extra logic yet.
            </p>
          </div>

          <RestaurantForm formData={formData} onChange={handleChange} />
        </section>

        <HealthCheckCard
          onCheck={handleHealthCheck}
          response={healthResponse}
          isLoading={isChecking}
          error={error}
        />
      </div>
    </main>
  );
}

export default DashboardPage;

