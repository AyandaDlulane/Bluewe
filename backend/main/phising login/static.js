class InternationalPhishGuardAuth {
    constructor(apiUrl = 'http://localhost:8000') {
        this.apiUrl = apiUrl;
        this.token = null;
        this.userLanguage = this.getBrowserLanguage();
    }

    getBrowserLanguage() {
        const lang = navigator.language || navigator.userLanguage;
        if (lang.startsWith('es')) return 'es';
        if (lang.startsWith('fr')) return 'fr';
        if (lang.startsWith('zh')) return 'zh';
        if (lang.startsWith('ar')) return 'ar';
        return 'en';
    }

    async setToken(token) {
        this.token = token;
        if (typeof chrome !== 'undefined' && chrome.storage) {
            await chrome.storage.local.set({phishguard_token: token});
        } else {
            localStorage.setItem('phishguard_token', token);
        }
    }

    async getToken() {
        if (this.token) return this.token;
        if (typeof chrome !== 'undefined' && chrome.storage) {
            const result = await chrome.storage.local.get(['phishguard_token']);
            this.token = result.phishguard_token;
        } else {
            this.token = localStorage.getItem('phishguard_token');
        }
        return this.token;
    }

    async login(username, password, language = null) {
        try {
            const lang = language || this.userLanguage;
            const response = await fetch(`${this.apiUrl}/api/auth/login`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ username, password, language: lang })
            });

            if (response.ok) {
                const data = await response.json();
                await this.setToken(data.token);
                this.userLanguage = data.language;
                return { success: true, user: data.user, message: data.message };
            } else {
                const error = await response.json();
                return { success: false, error: error.detail };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}