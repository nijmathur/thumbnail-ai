'use client'

import { useState } from 'react'
import { Sparkles, Mail, Check, ArrowRight } from 'lucide-react'

export default function ComingSoon() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // TODO: Connect to email service (ConvertKit, Mailchimp, etc.)
    // For now, just simulate success
    await new Promise(resolve => setTimeout(resolve, 1000))

    setSubmitted(true)
    setLoading(false)

    // Store in localStorage for now
    const existing = JSON.parse(localStorage.getItem('waitlist') || '[]')
    existing.push({ email, date: new Date().toISOString() })
    localStorage.setItem('waitlist', JSON.stringify(existing))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-8 h-8 text-red-500" />
            <h1 className="text-2xl font-bold">ThumbnailAI</h1>
          </div>
          <span className="bg-red-500/20 text-red-400 px-3 py-1 rounded-full text-sm font-medium">
            Coming Soon
          </span>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-20">
        {/* Hero */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-red-500/20 text-red-400 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4" />
            AI-Powered YouTube Thumbnails
          </div>

          <h2 className="text-5xl md:text-6xl font-bold mb-6">
            Generate Thumbnails in{' '}
            <span className="text-red-500">60 Seconds</span>
          </h2>

          <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
            Stop paying $30-100 per thumbnail. AI-powered generation with face consistency
            for personal branding. A/B test 10 variations for less than the cost of one designer thumbnail.
          </p>

          {/* Stats */}
          <div className="grid md:grid-cols-3 gap-6 max-w-3xl mx-auto mb-12">
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <div className="text-3xl font-bold text-red-500 mb-2">60 sec</div>
              <div className="text-gray-400">Generation time</div>
            </div>
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <div className="text-3xl font-bold text-red-500 mb-2">$0.01</div>
              <div className="text-gray-400">Per thumbnail</div>
            </div>
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <div className="text-3xl font-bold text-red-500 mb-2">99%</div>
              <div className="text-gray-400">Cost savings</div>
            </div>
          </div>
        </div>

        {/* Email Capture */}
        <div className="bg-gray-800 rounded-2xl p-8 md:p-12 border border-gray-700 mb-16">
          <h3 className="text-2xl font-bold text-center mb-4">
            Join the Waitlist
          </h3>
          <p className="text-gray-400 text-center mb-8">
            Get early access + 50% off your first 3 months. Limited spots available.
          </p>

          {submitted ? (
            <div className="flex items-center justify-center gap-3 text-green-400 bg-green-400/10 py-4 px-6 rounded-xl">
              <Check className="w-6 h-6" />
              <span className="font-medium">You&apos;re on the list! We&apos;ll be in touch soon.</span>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4 max-w-xl mx-auto">
              <div className="flex-1 relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full bg-gray-700 border border-gray-600 rounded-xl pl-12 pr-4 py-4 focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="bg-red-500 hover:bg-red-600 disabled:bg-gray-600 px-8 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors"
              >
                {loading ? (
                  'Joining...'
                ) : (
                  <>
                    Get Early Access
                    <ArrowRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </form>
          )}

          <p className="text-gray-500 text-sm text-center mt-4">
            No spam. Unsubscribe anytime.
          </p>
        </div>

        {/* Features Preview */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <div className="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-red-500" />
            </div>
            <h4 className="text-lg font-bold mb-2">AI Generation</h4>
            <p className="text-gray-400">
              Describe your thumbnail and watch AI create it in seconds. Multiple styles available.
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <div className="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-red-500" />
            </div>
            <h4 className="text-lg font-bold mb-2">Face Consistency</h4>
            <p className="text-gray-400">
              Your face stays the same across all thumbnails. Perfect for personal branding.
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <div className="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-red-500" />
            </div>
            <h4 className="text-lg font-bold mb-2">A/B Testing</h4>
            <p className="text-gray-400">
              Generate 10+ variations and test which performs best. Data-driven thumbnails.
            </p>
          </div>
        </div>

        {/* Pricing Preview */}
        <div className="mt-20">
          <h3 className="text-2xl font-bold text-center mb-8">Simple Pricing</h3>
          <div className="grid md:grid-cols-4 gap-4">
            {[
              { name: 'Starter', price: '$19', features: ['50 thumbnails', 'Basic templates', '720p'] },
              { name: 'Pro', price: '$29', features: ['150 thumbnails', 'Face consistency', '1080p', 'A/B testing'], popular: true },
              { name: 'Business', price: '$49', features: ['400 thumbnails', 'Priority gen', '4K', 'Analytics'] },
              { name: 'Enterprise', price: '$99', features: ['Unlimited', 'API access', 'White-label', 'Support'] },
            ].map((tier) => (
              <div
                key={tier.name}
                className={`bg-gray-800 p-6 rounded-xl border ${tier.popular ? 'border-red-500' : 'border-gray-700'}`}
              >
                {tier.popular && (
                  <div className="text-red-400 text-sm font-medium mb-2">Most Popular</div>
                )}
                <h4 className="text-xl font-bold mb-2">{tier.name}</h4>
                <div className="text-3xl font-bold mb-4">
                  {tier.price}
                  <span className="text-lg text-gray-500">/mo</span>
                </div>
                <ul className="space-y-2">
                  {tier.features.map((f, i) => (
                    <li key={i} className="text-gray-400 text-sm flex items-center gap-2">
                      <span className="text-red-500">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-700 py-8 text-center text-gray-500">
        <p>ThumbnailAI - AI-Powered YouTube Thumbnails</p>
        <p className="text-sm mt-2">
          Built with FLUX.1 AI • 99% cheaper than human designers
        </p>
      </footer>
    </div>
  )
}
