function Tabs({ tabs, activeTab, onChange }) {
  return (
    <div className="inline-flex rounded-2xl border border-orange-200 bg-orange-100/70 p-1">
      {tabs.map((tab) => {
        const isActive = tab === activeTab;

        return (
          <button
            key={tab}
            type="button"
            onClick={() => onChange(tab)}
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition-all duration-300 ${
              isActive
                ? "bg-red-500 text-white shadow-md"
                : "text-gray-700 hover:bg-white/70 hover:text-gray-900"
            }`}
          >
            {tab}
          </button>
        );
      })}
    </div>
  );
}

export default Tabs;
