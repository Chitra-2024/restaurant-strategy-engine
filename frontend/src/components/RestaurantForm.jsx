function RestaurantForm({ formData, onChange }) {
  const fields = [
    { id: "restaurantName", label: "Restaurant Name", type: "text", placeholder: "Enter restaurant name" },
    { id: "location", label: "Location", type: "text", placeholder: "Enter city or area" },
    { id: "dateRange", label: "Date Range", type: "text", placeholder: "e.g. 2026-03-01 to 2026-03-31" },
    { id: "zomatoUrl", label: "Zomato URL", type: "url", placeholder: "https://www.zomato.com/..." },
  ];

  return (
    <form className="grid gap-4 md:grid-cols-2">
      {fields.map((field) => (
        <label key={field.id} className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          {field.label}
          <input
            className="rounded-lg border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
            id={field.id}
            name={field.id}
            type={field.type}
            placeholder={field.placeholder}
            value={formData[field.id]}
            onChange={onChange}
          />
        </label>
      ))}
    </form>
  );
}

export default RestaurantForm;

