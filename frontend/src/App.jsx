import { useEffect, useState } from "react";

import DashboardPage from "./pages/DashboardPage";
import LandingPage from "./pages/LandingPage";
import { fetchReviewFeed, fetchStrategy } from "./services/api";

const LOADING_MESSAGES = [
  "Analyzing customer sentiment...",
  "Aggregating platform data...",
  "Generating strategic insights...",
];

function App() {
  const [page, setPage] = useState("landing");
  const [activeTab, setActiveTab] = useState("SWOT");
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);
  const [formData, setFormData] = useState({
    restaurant_name: "",
    location: "",
    days: 7,
  });
  const [strategyData, setStrategyData] = useState(null);
  const [reviewFeed, setReviewFeed] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isLoading) {
      return undefined;
    }

    const intervalId = window.setInterval(() => {
      setLoadingMessageIndex((current) => (current + 1) % LOADING_MESSAGES.length);
    }, 1400);

    return () => window.clearInterval(intervalId);
  }, [isLoading]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError("");
    setStrategyData(null);
    setReviewFeed([]);
    setLoadingMessageIndex(0);

    try {
      const [strategyResponse, reviewResponse] = await Promise.all([
        fetchStrategy(formData),
        fetchReviewFeed(formData),
      ]);

      if (strategyResponse.message) {
        setError(strategyResponse.message);
        setPage("landing");
        return;
      }

      setStrategyData(strategyResponse);
      setReviewFeed(reviewResponse.reviews ?? []);
      setActiveTab("SWOT");
      setPage("dashboard");
    } catch (requestError) {
      setError(requestError.message || "Unable to analyze this restaurant right now.");
      setPage("landing");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[linear-gradient(180deg,_#ffffff_0%,_#f8fafc_100%)] px-4">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-slate-200 border-t-slate-950" />
          <p className="mt-8 text-lg font-semibold text-slate-900">
            {LOADING_MESSAGES[loadingMessageIndex]}
          </p>
        </div>
      </main>
    );
  }

  if (page === "dashboard" && strategyData) {
    return (
      <DashboardPage
        restaurantName={formData.restaurant_name}
        strategyData={strategyData}
        reviewFeed={reviewFeed}
        formData={formData}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
    );
  }

  return (
    <LandingPage
      formData={formData}
      onChange={handleChange}
      onSubmit={handleSubmit}
      isLoading={isLoading}
      error={error}
    />
  );
}

export default App;
