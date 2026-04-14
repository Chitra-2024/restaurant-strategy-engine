function RestaurantForm({
  formData,
  onChange,
  onSubmit,
  isLoading,
  submitLabel = "Analyze",
}) {
  return (
    <form onSubmit={onSubmit} className="grid gap-4 lg:grid-cols-[1.6fr_1fr_0.7fr_auto] lg:items-end">
      <label>
        <span className="mb-2 block text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">
          Restaurant Name
        </span>
        <input
          className="w-full rounded-2xl border border-orange-200 bg-white px-5 py-4 text-base text-gray-800 shadow-md outline-none transition-all duration-300 focus:border-red-400 focus:ring-4 focus:ring-red-100"
          id="restaurant_name"
          name="restaurant_name"
          type="text"
          placeholder="Enter a restaurant to analyze"
          value={formData.restaurant_name}
          onChange={onChange}
          disabled={isLoading}
        />
      </label>

      <label>
        <span className="mb-2 block text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">
          Location
        </span>
        <input
          className="w-full rounded-2xl border border-orange-200 bg-white px-5 py-4 text-base text-gray-800 shadow-md outline-none transition-all duration-300 focus:border-red-400 focus:ring-4 focus:ring-red-100"
          id="location"
          name="location"
          type="text"
          placeholder="Optional city or area"
          value={formData.location}
          onChange={onChange}
          disabled={isLoading}
        />
      </label>

      <label>
        <span className="mb-2 block text-sm font-semibold uppercase tracking-[0.18em] text-gray-500">
          Days
        </span>
        <input
          className="w-full rounded-2xl border border-orange-200 bg-white px-5 py-4 text-base text-gray-800 shadow-md outline-none transition-all duration-300 focus:border-red-400 focus:ring-4 focus:ring-red-100"
          id="days"
          name="days"
          type="number"
          min="1"
          placeholder="7"
          value={formData.days}
          onChange={onChange}
          disabled={isLoading}
        />
      </label>

      <div className="flex flex-col gap-3 sm:flex-row lg:flex-col">
        <button
          type="submit"
          disabled={isLoading}
          className="inline-flex h-[58px] items-center justify-center rounded-xl bg-red-500 px-6 text-sm font-semibold uppercase tracking-[0.18em] text-white shadow-md transition-all duration-300 hover:bg-red-600 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? "Analyzing..." : submitLabel}
        </button>
      </div>
    </form>
  );
}

export default RestaurantForm;
