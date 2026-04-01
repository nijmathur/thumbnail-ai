'use client'

import { useState } from 'react'
import { Image, Zap, Layers, Upload, Download, Sparkles } from 'lucide-react'

const STYLES = [
  { id: 'youtube', name: 'YouTube', description: 'Bold, high-contrast clickbait style' },
  { id: 'minimal', name: 'Minimal', description: 'Clean, professional design' },
  { id: 'gaming', name: 'Gaming', description: 'Neon colors, dynamic action' },
  { id: 'tutorial', name: 'Tutorial', description: 'Educational, clear hierarchy' },
  { id: 'vlog', name: 'Vlog', description: 'Personal, authentic aesthetic' },
]

const RESOLUTIONS = [
  { id: '720p', name: '720p', badge: 'Starter' },
  { id: '1080p', name: '1080p', badge: 'Pro' },
  { id: '4K', name: '4K', badge: 'Business' },
]

export default function Home() {
  const [prompt, setPrompt] = useState('')
  const [style, setStyle] = useState('youtube')
  const [resolution, setResolution] = useState('1080p')
  const [textOverlay, setTextOverlay] = useState('')
  const [variations, setVariations] = useState(1)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<string[]>([])
  const [faceImage, setFaceImage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // Log request details
    console.log('=== THUMBNAIL GENERATION REQUEST ===')
    console.log('API URL:', process.env.NEXT_PUBLIC_API_URL)
    console.log('Request payload:', {
      prompt,
      style,
      resolution,
      text_overlay: textOverlay || undefined,
      variations,
      face_image_url: faceImage || undefined,
    })

    try {
      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/generate`
      console.log('Fetching:', apiUrl)

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          style,
          resolution,
          text_overlay: textOverlay || undefined,
          variations,
          face_image_url: faceImage || undefined,
        }),
      })

      console.log('Response status:', response.status, response.statusText)
      const data = await response.json()
      console.log('Response data:', data)

      if (response.ok && data.image_urls) {
        console.log('SUCCESS: Images generated:', data.image_urls)
        setResults(data.image_urls)
      } else {
        console.error('API Error:', data)
        alert(`Generation failed: ${data.detail || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Generation failed:', error)
      alert(`Generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setLoading(false)
      console.log('=== REQUEST COMPLETE ===')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary to-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold">ThumbnailAI</h1>
          </div>
          <nav className="flex gap-4">
            <a href="#features" className="text-gray-400 hover:text-white">Features</a>
            <a href="#pricing" className="text-gray-400 hover:text-white">Pricing</a>
            <button className="bg-primary hover:bg-red-600 px-4 py-2 rounded-lg font-medium">
              Get Started
            </button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-12">
        {/* Hero */}
        <section className="text-center mb-16">
          <h2 className="text-5xl font-bold mb-4">
            AI YouTube Thumbnails in <span className="text-primary">60 Seconds</span>
          </h2>
          <p className="text-xl text-gray-400 mb-8">
            Generate high-converting thumbnails with face consistency for personal branding.
            99% cheaper than human designers.
          </p>
          <div className="flex justify-center gap-4 text-sm text-gray-500">
            <span className="flex items-center gap-1"><Zap className="w-4 h-4" /> 60-second generation</span>
            <span className="flex items-center gap-1"><Layers className="w-4 h-4" /> A/B testing built-in</span>
            <span className="flex items-center gap-1"><Image className="w-4 h-4" /> Face consistency</span>
          </div>
        </section>

        {/* Generator */}
        <section className="grid lg:grid-cols-2 gap-8 mb-16">
          {/* Form */}
          <form onSubmit={handleSubmit} className="bg-gray-800 rounded-xl p-6 space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Thumbnail Description</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="A shocked person holding a laptop with money flying out, bright colors, YouTube style..."
                className="w-full bg-gray-700 rounded-lg p-3 h-32 focus:ring-2 focus:ring-primary outline-none"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Style</label>
              <div className="grid grid-cols-2 gap-2">
                {STYLES.map((s) => (
                  <button
                    key={s.id}
                    type="button"
                    onClick={() => setStyle(s.id)}
                    className={`p-3 rounded-lg text-left border ${
                      style === s.id
                        ? 'border-primary bg-gray-700'
                        : 'border-gray-700 hover:border-gray-600'
                    }`}
                  >
                    <div className="font-medium">{s.name}</div>
                    <div className="text-xs text-gray-500">{s.description}</div>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Resolution</label>
              <div className="flex gap-2">
                {RESOLUTIONS.map((r) => (
                  <button
                    key={r.id}
                    type="button"
                    onClick={() => setResolution(r.id)}
                    className={`flex-1 p-3 rounded-lg border ${
                      resolution === r.id
                        ? 'border-primary bg-gray-700'
                        : 'border-gray-700 hover:border-gray-600'
                    }`}
                  >
                    <div className="font-medium">{r.name}</div>
                    <div className="text-xs text-gray-500">{r.badge}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Text Overlay (optional)</label>
                <input
                  type="text"
                  value={textOverlay}
                  onChange={(e) => setTextOverlay(e.target.value)}
                  placeholder="$10,000 CHALLENGE"
                  className="w-full bg-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-primary outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Variations</label>
                <select
                  value={variations}
                  onChange={(e) => setVariations(Number(e.target.value))}
                  className="w-full bg-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-primary outline-none"
                >
                  {[1, 3, 5, 10].map((n) => (
                    <option key={n} value={n}>{n} variation{n > 1 ? 's' : ''}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Face Reference URL (for consistency)</label>
              <div className="flex gap-2">
                <input
                  type="url"
                  value={faceImage}
                  onChange={(e) => setFaceImage(e.target.value)}
                  placeholder="https://..."
                  className="flex-1 bg-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-primary outline-none"
                />
                <button type="button" className="p-3 bg-gray-700 rounded-lg hover:bg-gray-600">
                  <Upload className="w-5 h-5" />
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary hover:bg-red-600 disabled:bg-gray-600 py-4 rounded-lg font-bold text-lg flex items-center justify-center gap-2"
            >
              {loading ? (
                <>Generating...</>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Generate Thumbnail
                </>
              )}
            </button>
          </form>

          {/* Results */}
          <div className="bg-gray-800 rounded-xl p-6">
            <h3 className="text-lg font-medium mb-4">Results</h3>
            {results.length === 0 ? (
              <div className="h-96 flex items-center justify-center text-gray-500">
                <Image className="w-16 h-16" />
                <span className="ml-4">Your generated thumbnails will appear here</span>
              </div>
            ) : (
              <div className="grid gap-4">
                {results.map((url, i) => (
                  <div key={i} className="relative group">
                    <img src={url} alt={`Thumbnail ${i + 1}`} className="w-full rounded-lg" />
                    <a
                      href={url}
                      download
                      className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center gap-2 transition-opacity"
                    >
                      <Download className="w-6 h-6" />
                      Download
                    </a>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        {/* Features */}
        <section id="features" className="mb-16">
          <h3 className="text-3xl font-bold text-center mb-8">Why ThumbnailAI?</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-gray-800 p-6 rounded-xl">
              <Zap className="w-10 h-10 text-primary mb-4" />
              <h4 className="text-xl font-bold mb-2">60-Second Generation</h4>
              <p className="text-gray-400">From idea to thumbnail in under a minute. 45x faster than human designers.</p>
            </div>
            <div className="bg-gray-800 p-6 rounded-xl">
              <Image className="w-10 h-10 text-primary mb-4" />
              <h4 className="text-xl font-bold mb-2">Face Consistency</h4>
              <p className="text-gray-400">Your face stays the same across all thumbnails. Perfect for personal branding.</p>
            </div>
            <div className="bg-gray-800 p-6 rounded-xl">
              <Layers className="w-10 h-10 text-primary mb-4" />
              <h4 className="text-xl font-bold mb-2">A/B Testing</h4>
              <p className="text-gray-400">Generate 10-15 variations per video. Test and optimize for maximum CTR.</p>
            </div>
          </div>
        </section>

        {/* Pricing */}
        <section id="pricing" className="mb-16">
          <h3 className="text-3xl font-bold text-center mb-8">Simple Pricing</h3>
          <div className="grid md:grid-cols-4 gap-4">
            {[
              { name: 'Starter', price: '$19', features: ['50 thumbnails/month', 'Basic templates', '720p resolution'] },
              { name: 'Pro', price: '$29', features: ['150 thumbnails/month', 'Face consistency', '1080p', 'A/B testing'], popular: true },
              { name: 'Business', price: '$49', features: ['400 thumbnails/month', 'Priority generation', '4K resolution', 'Analytics'] },
              { name: 'Enterprise', price: '$99', features: ['Unlimited thumbnails', 'API access', 'White-label', 'Dedicated support'] },
            ].map((tier) => (
              <div
                key={tier.name}
                className={`bg-gray-800 p-6 rounded-xl border ${tier.popular ? 'border-primary' : 'border-gray-700'}`}
              >
                {tier.popular && <div className="text-primary text-sm font-medium mb-2">Most Popular</div>}
                <h4 className="text-xl font-bold mb-2">{tier.name}</h4>
                <div className="text-4xl font-bold mb-4">{tier.price}<span className="text-lg text-gray-500">/mo</span></div>
                <ul className="space-y-2 mb-6">
                  {tier.features.map((f) => (
                    <li key={f} className="text-gray-400 flex items-center gap-2">
                      <span className="text-primary">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
                <button className="w-full bg-primary hover:bg-red-600 py-2 rounded-lg font-medium">
                  Get Started
                </button>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8 text-center text-gray-500">
        <p>ThumbnailAI - Automated Business Scout Implementation</p>
        <p className="text-sm mt-2">Feasibility Score: 8.2/10 | Break-even: 350-450 customers</p>
      </footer>
    </div>
  )
}
