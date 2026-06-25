# translations.py
# Dicionário central de traduções do app
# Adicione novas chaves aqui conforme criar novas páginas

TRANSLATIONS = {

    # ── Global / Sidebar ──────────────────────────────────────────────────────
    "lang_label":        {"pt": "🌐 Idioma",          "en": "🌐 Language"},
    "lang_pt":           {"pt": "🇧🇷 Português",       "en": "🇧🇷 Portuguese"},
    "lang_en":           {"pt": "🇺🇸 Inglês",          "en": "🇺🇸 English"},

    # ── Gym page ──────────────────────────────────────────────────────────────
    "gym_title":         {"pt": "💪 Academia",              "en": "💪 Gym"},
    "gym_training":      {"pt": "💪 Treino:",          "en": "💪 Training:"},
    "gym_series":        {"pt": "🏋️ Série:",         "en": "🏋️ Serie:"},
    "gym_break":         {"pt": "⏰ Descanso:",        "en": "⏰ Break:"},
    "gym_start":         {"pt": "▶️ Iniciar",          "en": "▶️ Start"},
    "gym_save":          {"pt": "💾 Salvar",           "en": "💾 Save"},
    "gym_done":          {"pt": "Feito",               "en": "Done"},
    "gym_weight":        {"pt": "Peso",                "en": "Weight"},
    "gym_3weeks":        {"pt": "3 Semanas",           "en": "3 Weeks"},
    "gym_last":          {"pt": "Último",              "en": "Last"},
    "gym_now":           {"pt": "Agora",               "en": "Now"},
    "gym_proposition":   {"pt": "Proposta",             "en": "Proposition"},
    "gym_dif":           {"pt": "Dif",                 "en": "Dif"},
    "gym_up":            {"pt": "Aumento",               "en": "Raise"},

    # ── Diet page ─────────────────────────────────────────────────────────────
    "diet_title":        {"pt": "🥗 Plano Alimentar",  "en": "🥗 Meal Plan"},
    "diet_meal":         {"pt": "🍽️ Refeição:",       "en": "🍽️ Meal:"},
    "diet_date":         {"pt": "📅 Data:",            "en": "📅 Date:"},
    "diet_all":          {"pt": "Todas",               "en": "All"},
    "diet_summary":      {"pt": "📊 Resumo do Dia",    "en": "📊 Daily Summary"},
    "diet_calories":     {"pt": "🔥 Calorias",         "en": "🔥 Calories"},
    "diet_protein":      {"pt": "💪 Proteína",         "en": "💪 Protein"},
    "diet_carbs":        {"pt": "🍞 Carboidrato",      "en": "🍞 Carbs"},
    "diet_fat":          {"pt": "🥑 Gordura",          "en": "🥑 Fat"},
    "diet_meals":        {"pt": "### 🍽️ Refeições",   "en": "### 🍽️ Meals"},
    "diet_qty":          {"pt": "Qtd (g/ml)",          "en": "Qty (g/ml)"},
    "diet_save":         {"pt": "💾 Salvar",           "en": "💾 Save"},
    "diet_evolution":    {"pt": "### 📈 Evolução de Calorias", "en": "### 📈 Calorie Evolution"},
    "diet_macro_table":  {"pt": "### 🧾 Macros por Refeição", "en": "### 🧾 Macros per Meal"},
    "diet_new_food":     {"pt": "### 🤖 Adicionar Alimento com IA", "en": "### 🤖 Add Food with AI"},
    "diet_new_expander": {"pt": "➕ Novo alimento (IA estima os macros)", "en": "➕ New food (AI estimates macros)"},
    "diet_food_name":    {"pt": "Nome do alimento",    "en": "Food name"},
    "diet_food_ph":      {"pt": "ex: peito de frango grelhado", "en": "e.g. grilled chicken breast"},
    "diet_estimate_btn": {"pt": "🤖 Estimar macros com IA", "en": "🤖 Estimate macros with AI"},
    "diet_estimating":   {"pt": "IA calculando macros...", "en": "AI calculating macros..."},
    "diet_no_food":      {"pt": "Digite o nome do alimento.", "en": "Please enter the food name."},
    "diet_ia_tip":       {"pt": "💡 IA:",              "en": "💡 AI:"},
    "diet_cal_calc":     {"pt": "🔥 Calorias (calculadas)", "en": "🔥 Calories (calculated)"},
    "diet_save_new":     {"pt": "💾 Salvar novo alimento", "en": "💾 Save new food"},
    "diet_saved_ok":     {"pt": "✅ salvo com",        "en": "✅ saved with"},
    "diet_kcal":         {"pt": "kcal!",               "en": "kcal!"},
    "diet_ia_btn":       {"pt": "🤖 IA",               "en": "🤖 AI"},
    "diet_ia_spinner":   {"pt": "IA buscando macros...", "en": "AI fetching macros..."},
    "diet_ia_caption":   {"pt": "🤖 IA estimou os macros para", "en": "🤖 AI estimated macros for"},
    "diet_prot_field":   {"pt": "💪 Proteína (g)",     "en": "💪 Protein (g)"},
    "diet_carb_field":   {"pt": "🍞 Carbo (g)",        "en": "🍞 Carbs (g)"},
    "diet_fat_field":    {"pt": "🥑 Gordura (g)",      "en": "🥑 Fat (g)"},
    "diet_cal_metric":   {"pt": "🔥 Calorias",         "en": "🔥 Calories"},

    "meal_breakfast":    {"pt": "Café da manhã",       "en": "Breakfast"},
    "meal_morning":      {"pt": "Lanche da manhã",     "en": "Morning Snack"},
    "meal_lunch":        {"pt": "Almoço",              "en": "Lunch"},
    "meal_afternoon":    {"pt": "Lanche da tarde",     "en": "Afternoon Snack"},
    "meal_dinner":       {"pt": "Jantar",              "en": "Dinner"},
    "meal_supper":       {"pt": "Ceia",                "en": "Late Snack"},
}


def t(key: str, lang: str) -> str:
    """Retorna o texto traduzido para a chave e idioma dados."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key  # fallback: retorna a própria chave
    return entry.get(lang, entry.get("pt", key))


def meal_names(lang: str) -> list:
    """Retorna a lista de nomes de refeições no idioma correto."""
    keys = ["meal_breakfast","meal_morning","meal_lunch","meal_afternoon","meal_dinner","meal_supper"]
    return [t(k, lang) for k in keys]
