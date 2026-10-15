import { useState } from 'react'
import './App.css'


const translations = {
  en: {
    intelligence: 'PRODUCTION INTELLIGENCE',
    title: 'Production Issue Analysis',
    subtitle: 'Report a production issue and receive an AI-assisted analysis.',

    newAnalysis: 'New Analysis',
    reports: 'Reports',
    analytics: 'Analytics',
    systemOnline: 'System Online',
    cloud: 'Azure Cloud',

    issueDetails: 'Issue Details',
    productionReport: 'Production Report',

    problemType: 'Problem Type',
    problemTypePlaceholder: 'e.g. Pressure fluctuation',

    problemDescription: 'Problem Description',
    problemDescriptionPlaceholder: 'Describe the production issue...',

    processParameters: 'Process Parameters',

    downtime: 'Downtime',
    temperature: 'Temperature',
    pressure: 'Injection Pressure',
    cycleTime: 'Cycle Time',

    operatorComment: 'Operator Comment',
    operatorCommentPlaceholder: 'Additional observations...',

    analyze: 'Analyze with AI',
    analyzing: 'Analyzing...',

    aiAnalysis: 'AI Analysis',
    aiAssisted: 'AI Assisted',

    ready: 'Ready for analysis',
    readyText:
      'Submit a production issue to generate an AI-supported assessment.',

    severity: 'Severity',
    cause: 'Cause',
    action: 'Action',

    report: 'REPORT',
    category: 'Category',
    confidence: 'Confidence',

    possibleCause: 'POSSIBLE CAUSE',
    recommendedAction: 'RECOMMENDED ACTION',

    low: 'LOW',
    medium: 'MEDIUM',
    high: 'HIGH',

    error: 'The analysis could not be completed. Please try again.',

    changeLanguage: 'Language'
  },

  de: {
    intelligence: 'PRODUKTIONSINTELLIGENZ',
    title: 'Analyse von Produktionsproblemen',
    subtitle:
      'Produktionsproblem melden und eine KI-gestützte Analyse erhalten.',

    newAnalysis: 'Neue Analyse',
    reports: 'Berichte',
    analytics: 'Auswertungen',
    systemOnline: 'System online',
    cloud: 'Azure Cloud',

    issueDetails: 'Problemdetails',
    productionReport: 'Produktionsbericht',

    problemType: 'Problemart',
    problemTypePlaceholder: 'z. B. Druckschwankung',

    problemDescription: 'Problembeschreibung',
    problemDescriptionPlaceholder: 'Produktionsproblem beschreiben...',

    processParameters: 'Prozessparameter',

    downtime: 'Stillstandszeit',
    temperature: 'Temperatur',
    pressure: 'Einspritzdruck',
    cycleTime: 'Zykluszeit',

    operatorComment: 'Kommentar des Bedieners',
    operatorCommentPlaceholder: 'Weitere Beobachtungen...',

    analyze: 'Mit KI analysieren',
    analyzing: 'Analyse läuft...',

    aiAnalysis: 'KI-Analyse',
    aiAssisted: 'KI-gestützt',

    ready: 'Bereit für die Analyse',
    readyText:
      'Produktionsproblem absenden, um eine KI-gestützte Bewertung zu erhalten.',

    severity: 'Schweregrad',
    cause: 'Ursache',
    action: 'Maßnahme',

    report: 'BERICHT',
    category: 'Kategorie',
    confidence: 'Konfidenz',

    possibleCause: 'MÖGLICHE URSACHE',
    recommendedAction: 'EMPFOHLENE MASSNAHME',

    low: 'NIEDRIG',
    medium: 'MITTEL',
    high: 'HOCH',

    error:
      'Die Analyse konnte nicht abgeschlossen werden. Bitte erneut versuchen.',

    changeLanguage: 'Sprache'
  }
}


function App() {

  const [language, setLanguage] = useState(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

const [loginData, setLoginData] = useState({
  email: '',
  password: ''
})
  const [token, setToken] = useState(null)
const [role, setRole] = useState(null)
const [loginError, setLoginError] = useState('')
const [activePage, setActivePage] = useState('analysis')
  const [selectedReport, setSelectedReport] = useState(null)
  const [formData, setFormData] = useState({
    problem_type: '',
    problem_description: '',
    downtime: '',
    temperature: '',
    pressure: '',
    cycle_time: '',
    comment: ''
  })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [reports, setReports] = useState([])
const [reportsLoading, setReportsLoading] = useState(false)


  if (!language) {
    return (
      <div className="language-screen">

        <div className="language-card">

          <div className="language-logo">
            AI
          </div>

          <p className="language-eyebrow">
            INDUSTRIAL AI PLATFORM
          </p>

          <h1>
            AI Production Issue System
          </h1>

          <p className="language-subtitle">
            Select your language
            <br />
            Sprache auswählen
          </p>


          <div className="language-options">

            <button
              className="language-option"
              onClick={() => setLanguage('de')}
            >
              <span className="flag">🇩🇪</span>

              <div>
                <strong>Deutsch</strong>
                <span>Deutschland</span>
              </div>
            </button>


            <button
              className="language-option"
              onClick={() => setLanguage('en')}
            >
              <span className="flag">🇬🇧</span>

              <div>
                <strong>English</strong>
                <span>United Kingdom</span>
              </div>
            </button>

          </div>


          <div className="language-footer">
            AI-assisted production intelligence
          </div>

        </div>

      </div>
    )
  }

if (language && !isLoggedIn) {
  return (
    <div className="language-screen">

      <div className="login-card">

        <div className="language-logo">
          AI
        </div>

        <p className="language-eyebrow">
          {language === 'de'
            ? 'SICHERER ZUGANG'
            : 'SECURE ACCESS'}
        </p>

        <h1>
          {language === 'de'
            ? 'Willkommen zurück'
            : 'Welcome back'}
        </h1>

        <p className="login-subtitle">
          {language === 'de'
            ? 'Melden Sie sich an, um auf Ihren Arbeitsbereich zuzugreifen.'
            : 'Sign in to access your production workspace.'}
        </p>

        <form

  className="login-form"
  onSubmit={handleLogin}
>

  <div className="login-field">
    <label>
      {language === 'de' ? 'E-Mail-Adresse' : 'Email address'}
    </label>

    <input
      type="email"
      value={loginData.email}
      onChange={(event) =>
        setLoginData({
          ...loginData,
          email: event.target.value
        })
      }
      placeholder="name@factory.com"
      required
    />
  </div>

  <div className="login-field">
    <label>
      {language === 'de' ? 'Passwort' : 'Password'}
    </label>

    <input
      type="password"
      value={loginData.password}
      onChange={(event) =>
        setLoginData({
          ...loginData,
          password: event.target.value
        })
      }
      placeholder="••••••••"
      required
    />
  </div>

  <button
    className="login-button"
    type="submit"
  >
    {language === 'de'
      ? 'Anmelden'
      : 'Sign in'}

    <span>→</span>
  </button>

</form>
        <button
          className="back-language-button"
          onClick={() => setLanguage(null)}
        >
          ← {language === 'de'
            ? 'Sprache ändern'
            : 'Change language'}
        </button>

        <div className="language-footer">
          AI Production Issue Management
        </div>

      </div>

    </div>
  )
}
  const t = translations[language]

async function handleLogin(event) {
  event.preventDefault()

  setLoginError('')

  try {
    const response = await fetch(
  'https://ai-production-api.greenhill-61f34f6f.polandcentral.azurecontainerapps.io/auth/login',
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify(loginData)
      }
    )

    if (!response.ok) {
      throw new Error('Login failed')
    }

    const data = await response.json()

    setToken(data.access_token)
    setRole(data.role)
    setIsLoggedIn(true)

  } catch (error) {
    setLoginError(
      language === 'de'
        ? 'E-Mail-Adresse oder Passwort ist ungültig.'
        : 'Invalid email or password.'
    )
  }
}
async function loadReports() {
  setReportsLoading(true)

  try {
    const response = await fetch(
      'https://ai-production-api.greenhill-61f34f6f.polandcentral.azurecontainerapps.io/reports',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    if (!response.ok) {
      throw new Error('Failed to load reports')
    }

    const data = await response.json()
    setReports(data)

  } catch (error) {
    console.error(error)

  } finally {
    setReportsLoading(false)
  }
}
async function loadReportDetail(reportId) {
  try {
    const response = await fetch(
      `https://ai-production-api.greenhill-61f34f6f.polandcentral.azurecontainerapps.io/reports/${reportId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    if (!response.ok) {
      throw new Error('Failed to load report detail')
    }

    const data = await response.json()

    setSelectedReport(data)

  } catch (error) {
    console.error(error)
  }
}

async function updateReportStatus(newStatus) {
  if (!selectedReport) return

  try {
    const response = await fetch(
      `https://ai-production-api.greenhill-61f34f6f.polandcentral.azurecontainerapps.io/reports/${selectedReport.report_id}/status`,
      {
        method: 'PATCH',

        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },

        body: JSON.stringify({
          status: newStatus
        })
      }
    )

    if (!response.ok) {
      throw new Error('Failed to update report status')
    }

    const data = await response.json()

    setSelectedReport({
      ...selectedReport,
      status: data.status
    })

  } catch (error) {
    console.error(error)
  }
}

  function handleChange(event) {

    const { name, value } = event.target

    setFormData({
      ...formData,
      [name]: value
    })
  }


  async function handleSubmit(event) {

    event.preventDefault()

    setLoading(true)
    setError('')
    setResult(null)

    try {

      const response = await fetch(
        'https://ai-production-api.greenhill-61f34f6f.polandcentral.azurecontainerapps.io/analyze',
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            ...formData,
            ui_language: language
          })
        }
      )


      if (!response.ok) {
        throw new Error('Analysis failed')
      }


      const data = await response.json()

      setResult(data)

    } catch (error) {

      setError(t.error)

    } finally {

      setLoading(false)
    }
  }


  function getSeverityClass(severity) {

    if (!severity) return ''

    return severity.toLowerCase()
  }


  function displaySeverity(severity) {

    if (!severity) return ''

    if (severity === 'LOW') {
      return t.low
    }

    if (severity === 'MEDIUM') {
      return t.medium
    }

    if (severity === 'HIGH') {
      return t.high
    }

    return severity
  }


  function displayCategory(category) {

    if (language === 'en') {
      return category
    }

    const categoryTranslations = {
      Process: 'Prozess',
      Quality: 'Qualität',
      Safety: 'Sicherheit',
      Maintenance: 'Instandhaltung',
      Equipment: 'Anlage',
      Production: 'Produktion'
    }

    return categoryTranslations[category] || category
  }


  return (

    <div className="app">


      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            AI
          </div>

          <div>
            <h2>Production AI</h2>
            <span>Issue Management</span>
          </div>

        </div>


        <nav>

          <button
  className={`nav-item ${activePage === 'analysis' ? 'active' : ''}`}
  onClick={() => setActivePage('analysis')}
>
  <span>01</span>
  {t.newAnalysis}
</button>

         {role === 'engineer' && (
  <>
    <button
      className={`nav-item ${activePage === 'reports' ? 'active' : ''}`}
      onClick={() => {
        setActivePage('reports')
        loadReports()
      }}
    >
      <span>02</span>
      {t.reports}
    </button>
  </>
)}

        </nav>


        <div className="sidebar-footer">

          <div className="system-status">

            <span className="status-dot"></span>

            {t.systemOnline}

          </div>

          <small>
            AI Production System
          </small>

        </div>

      </aside>


      <main className="main-content">


        <header className="topbar">

          <div>

            <p className="eyebrow">
              {t.intelligence}
            </p>

            <h1>
              {t.title}
            </h1>

            <p className="subtitle">
              {t.subtitle}
            </p>

          </div>


          <div className="top-actions">

            <button
              className="language-switch"
              onClick={() => setLanguage(null)}
            >

              <span>
                {language === 'de' ? '🇩🇪' : '🇬🇧'}
              </span>

              {t.changeLanguage}

            </button>


            <div className="cloud-status">

              <span className="cloud-dot"></span>

              {t.cloud}

            </div>

          </div>

        </header>

{activePage === 'reports' && (
  <div className="reports-page">
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="step">02</span>
          <h2>{t.reports}</h2>
        </div>
      </div>

      {reportsLoading ? (
  <p>Loading reports...</p>
) : reports.length === 0 ? (
  <p>No reports found.</p>
) : (
  <div className="reports-table-wrapper">

  <table className="reports-table">

    <thead>
      <tr>
        <th>Report ID</th>
        <th>Date</th>
        <th>Problem Type</th>
        <th>Severity</th>
        <th>Confidence</th>
        <th>Action</th>
      </tr>
    </thead>

    <tbody>

      {reports.map((report) => (
        <tr key={report.report_id}>

          <td>
            <strong>{report.report_id}</strong>
          </td>

          <td>
            {new Date(report.timestamp).toLocaleString()}
          </td>

          <td>
            {report.problem_type}
          </td>

          <td>
            <span
              className={`severity ${getSeverityClass(report.severity)}`}
            >
              {displaySeverity(report.severity)}
            </span>
          </td>

          <td>
            {report.confidence}%
          </td>

          <td>
            <button
              className="view-report-button"
              onClick={() => loadReportDetail(report.report_id)}
            >
              View Report
            </button>
          </td>

        </tr>
      ))}

    </tbody>

  </table>

</div>
          )}

      {selectedReport && (
  <div className="panel report-detail">

    <div className="panel-header">
      <div>
        <span className="step">03</span>
        <h2>Report Detail</h2>
      </div>

      <span className={`severity ${getSeverityClass(selectedReport.severity)}`}>
        {displaySeverity(selectedReport.severity)}
      </span>
    </div>

    <div className="metrics">

      <div className="metric">
        <span>Report ID</span>
        <strong>{selectedReport.report_id}</strong>
      </div>

      <div className="metric">
  <span>Status</span>

  <div className="status-buttons">

    <button
      onClick={() => updateReportStatus('OPEN')}
      disabled={selectedReport.status === 'OPEN'}
    >
      🔴 OPEN
    </button>

    <button
      onClick={() => updateReportStatus('UNDER_REVIEW')}
      disabled={selectedReport.status === 'UNDER_REVIEW'}
    >
      🟡 UNDER REVIEW
    </button>

    <button
      onClick={() => updateReportStatus('RESOLVED')}
      disabled={selectedReport.status === 'RESOLVED'}
    >
      🟢 RESOLVED
    </button>

  </div>
</div>

      <div className="metric">
        <span>Category</span>
        <strong>{displayCategory(selectedReport.category)}</strong>
      </div>

      <div className="metric">
        <span>Confidence</span>
        <strong>{selectedReport.confidence}%</strong>
      </div>

    </div>

    <div className="analysis-block">
      <span className="block-label">PROBLEM DESCRIPTION</span>
      <p>{selectedReport.problem_description}</p>
    </div>

    <div className="analysis-block">
      <span className="block-label">POSSIBLE CAUSE</span>
      <p>{selectedReport.possible_cause}</p>
    </div>

    <div className="analysis-block recommendation">
      <span className="block-label">RECOMMENDED ACTION</span>
      <p>{selectedReport.recommended_action}</p>
    </div>

  </div>
)}
    </div>
  </div>
)}
        {activePage === 'analysis' && (
  <div className="content-grid">


          <section className="panel form-panel">

            <div className="panel-header">

              <div>

                <span className="step">
                  01
                </span>

                <h2>
                  {t.issueDetails}
                </h2>

              </div>

              <span className="required-label">
                {t.productionReport}
              </span>

            </div>


            <form onSubmit={handleSubmit}>


              <div className="field full-width">

                <label>
                  {t.problemType}
                </label>

                <input
                  type="text"
                  name="problem_type"
                  placeholder={t.problemTypePlaceholder}
                  value={formData.problem_type}
                  onChange={handleChange}
                  required
                />

              </div>


              <div className="field full-width">

                <label>
                  {t.problemDescription}
                </label>

                <textarea
                  name="problem_description"
                  placeholder={t.problemDescriptionPlaceholder}
                  value={formData.problem_description}
                  onChange={handleChange}
                  required
                />

              </div>


              <div className="parameter-title">
                {t.processParameters}
              </div>


              <div className="form-grid">


                <div className="field">

                  <label>
                    {t.downtime}
                  </label>

                  <div className="input-unit">

                    <input
                      type="number"
                      name="downtime"
                      placeholder="0"
                      value={formData.downtime}
                      onChange={handleChange}
                    />

                    <span>min</span>

                  </div>

                </div>


                <div className="field">

                  <label>
                    {t.temperature}
                  </label>

                  <div className="input-unit">

                    <input
                      type="number"
                      name="temperature"
                      placeholder="220"
                      value={formData.temperature}
                      onChange={handleChange}
                    />

                    <span>°C</span>

                  </div>

                </div>


                <div className="field">

                  <label>
                    {t.pressure}
                  </label>

                  <div className="input-unit">

                    <input
                      type="number"
                      name="pressure"
                      placeholder="80"
                      value={formData.pressure}
                      onChange={handleChange}
                    />

                    <span>bar</span>

                  </div>

                </div>


                <div className="field">

                  <label>
                    {t.cycleTime}
                  </label>

                  <div className="input-unit">

                    <input
                      type="number"
                      name="cycle_time"
                      placeholder="42"
                      value={formData.cycle_time}
                      onChange={handleChange}
                    />

                    <span>sec</span>

                  </div>

                </div>


              </div>


              <div className="field full-width">

                <label>
                  {t.operatorComment}
                </label>

                <textarea
                  className="small-textarea"
                  name="comment"
                  placeholder={t.operatorCommentPlaceholder}
                  value={formData.comment}
                  onChange={handleChange}
                />

              </div>


              <button
                className="analyze-button"
                type="submit"
                disabled={loading}
              >

                {loading ? (
                  <>
                    <span className="spinner"></span>
                    {t.analyzing}
                  </>
                ) : (
                  <>
                    {t.analyze}
                    <span className="arrow">→</span>
                  </>
                )}

              </button>


            </form>

          </section>


          <section className="panel analysis-panel">


            <div className="panel-header">

              <div>

                <span className="step">
                  02
                </span>

                <h2>
                  {t.aiAnalysis}
                </h2>

              </div>

              <span className="ai-label">
                {t.aiAssisted}
              </span>

            </div>


            {!result && !loading && !error && (

              <div className="empty-state">

                <div className="analysis-symbol">
                  AI
                </div>

                <h3>
                  {t.ready}
                </h3>

                <p>
                  {t.readyText}
                </p>


                <div className="analysis-features">

                  <span>
                    {t.severity}
                  </span>

                  <span>
                    {t.cause}
                  </span>

                  <span>
                    {t.action}
                  </span>

                </div>

              </div>

            )}


            {loading && (

              <div className="loading-state">

                <div className="loading-ring"></div>

                <h3>
                  {t.analyzing}
                </h3>

              </div>

            )}


            {error && (

              <div className="error-card">
                {error}
              </div>

            )}


            {result && (

  <div className="result">

    <div className="result-top">

      <div>
        <span className="result-label">
          {t.report}
        </span>

        <strong>
          {result.report_id}
        </strong>
      </div>

      <span
        className={`severity ${getSeverityClass(
          result.severity
        )}`}
      >
        {displaySeverity(
          result.severity
        )}
      </span>

    </div>


    <div className="metrics">

      <div className="metric">
        <span>
          {t.category}
        </span>

        <strong>
          {displayCategory(
            result.category
          )}
        </strong>
      </div>


      <div className="metric">
        <span>
          {t.confidence}
        </span>

        <strong>
          {result.confidence}%
        </strong>
      </div>

    </div>


    <div className="analysis-block">

      <span className="block-label">
        {t.severity}
      </span>

      <p>
        <strong>
          {displaySeverity(result.severity)}
        </strong>
      </p>

      <p>
        <strong>Reference:</strong>{' '}
        {result.severity_reference || 'Not available'}
      </p>

      <p>
        <strong>Source:</strong>{' '}
        {result.sources?.severity?.join(', ') || 'Not available'}
      </p>

    </div>


    <div className="analysis-block">

      <span className="block-label">
        {t.possibleCause}
      </span>

      <p>
        {result.display_possible_cause
          || result.possible_cause
          || 'Not available'}
      </p>

      <p>
        <strong>Reference:</strong>{' '}
        {result.possible_cause_reference || 'Not available'}
      </p>

      <p>
        <strong>Source:</strong>{' '}
        {result.sources?.possible_cause?.join(', ') || 'Not available'}
      </p>

    </div>


    <div className="analysis-block recommendation">

      <span className="block-label">
        {t.recommendedAction}
      </span>

      <p>
        {result.display_recommended_action
          || result.recommended_action
          || 'Not available'}
      </p>

      <p>
        <strong>Reference:</strong>{' '}
        {result.recommended_action_reference || 'Not available'}
      </p>

      <p>
        <strong>Source:</strong>{' '}
        {result.sources?.recommended_action?.join(', ') || 'Not available'}
      </p>

    </div>

  </div>

)}
          </section>

        </div>
      )}
      </main>

    </div>

  )
}


export default App