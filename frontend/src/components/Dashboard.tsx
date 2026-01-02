// src/components/Dashboard.tsx

"use client";

import { supabase } from "@/lib/supabase";
import { User } from "@supabase/supabase-js";
import { useState, useEffect } from "react";

interface DashboardProps {
  user: User;
}

const SKILLS_OPTIONS = [
  "Python", "Semantic Kernel", "Azure OpenAI", "Machine Learning",
  "Data Analysis", "Cloud Computing", "JavaScript", "React",
  "Node.js", "LLM", "Prompt Engineering", "Data Science",
  "DevOps", "SQL", "TypeScript", "FastAPI", "AWS", "Docker",
  "Kubernetes", "TensorFlow", "PyTorch", "NLP", "Computer Vision",
  "Git", "CI/CD", "Agile", "Scrum", "Java", "C++", "Rust", "Go"
];

// Rocket Launch Animation Component
const RocketLaunchAnimation = ({ onComplete }: { onComplete: () => void }) => {
  const [phase, setPhase] = useState<'countdown' | 'launch' | 'flying' | 'complete'>('countdown');
  const [count, setCount] = useState(3);

  useEffect(() => {
    if (phase === 'countdown') {
      if (count > 0) {
        const timer = setTimeout(() => setCount(count - 1), 800);
        return () => clearTimeout(timer);
      } else {
        setPhase('launch');
      }
    } else if (phase === 'launch') {
      const timer = setTimeout(() => setPhase('flying'), 500);
      return () => clearTimeout(timer);
    } else if (phase === 'flying') {
      const timer = setTimeout(() => setPhase('complete'), 1500);
      return () => clearTimeout(timer);
    } else if (phase === 'complete') {
      const timer = setTimeout(() => onComplete(), 500);
      return () => clearTimeout(timer);
    }
  }, [phase, count, onComplete]);

  return (
    <div className="fixed inset-0 bg-gradient-to-b from-slate-900 via-indigo-950 to-slate-900 flex items-center justify-center z-50 overflow-hidden">
      {/* Stars Background */}
      <div className="absolute inset-0">
        {[...Array(50)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-white rounded-full animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 2}s`,
              opacity: Math.random() * 0.8 + 0.2,
            }}
          />
        ))}
      </div>

      {/* Rocket */}
      <div
        className={`relative transition-all duration-1000 ease-in-out ${
          phase === 'countdown' ? 'translate-y-0' :
          phase === 'launch' ? '-translate-y-10 scale-110' :
          phase === 'flying' ? '-translate-y-[800px] scale-75' :
          '-translate-y-[1000px] opacity-0'
        }`}
      >
        {/* Rocket SVG */}
        <svg width="120" height="120" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg" className="drop-shadow-2xl">
          <defs>
            <linearGradient id="rocketGradientAnim" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#6366F1" />
              <stop offset="50%" stopColor="#8B5CF6" />
              <stop offset="100%" stopColor="#A855F7" />
            </linearGradient>
            <linearGradient id="flameGradientAnim" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#FBBF24" />
              <stop offset="50%" stopColor="#F97316" />
              <stop offset="100%" stopColor="#EF4444" />
            </linearGradient>
            <linearGradient id="windowGradientAnim" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#38BDF8" />
              <stop offset="100%" stopColor="#0EA5E9" />
            </linearGradient>
          </defs>
          
          <circle cx="28" cy="28" r="26" fill="url(#rocketGradientAnim)" opacity="0.1"/>
          <path d="M28 8C28 8 38 18 38 30C38 38 34 44 28 46C22 44 18 38 18 30C18 18 28 8 28 8Z" 
                fill="url(#rocketGradientAnim)" />
          <circle cx="28" cy="24" r="6" fill="url(#windowGradientAnim)" />
          <circle cx="28" cy="24" r="4" fill="#1E293B" />
          <circle cx="26" cy="22" r="1.5" fill="#38BDF8" opacity="0.6" />
          <path d="M18 34L12 42L18 40V34Z" fill="url(#rocketGradientAnim)" />
          <path d="M38 34L44 42L38 40V34Z" fill="url(#rocketGradientAnim)" />
          
          {/* Animated Flame */}
          {phase !== 'countdown' && (
            <>
              <ellipse cx="28" cy="52" rx="8" ry="6" fill="url(#flameGradientAnim)" className="animate-pulse" />
              <ellipse cx="28" cy="50" rx="5" ry="4" fill="#FBBF24" className="animate-pulse" />
              <ellipse cx="28" cy="48" rx="3" ry="3" fill="#FEF3C7" />
            </>
          )}
        </svg>

        {/* Smoke/Exhaust */}
        {phase === 'launch' || phase === 'flying' ? (
          <div className="absolute top-full left-1/2 -translate-x-1/2">
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className="absolute w-4 h-4 bg-gray-400 rounded-full animate-ping opacity-50"
                style={{
                  left: `${(Math.random() - 0.5) * 40}px`,
                  top: `${i * 15}px`,
                  animationDelay: `${i * 0.1}s`,
                  animationDuration: '0.8s',
                }}
              />
            ))}
          </div>
        ) : null}
      </div>

      {/* Countdown Text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        {phase === 'countdown' && count > 0 && (
          <div className="text-8xl font-bold text-white animate-bounce">
            {count}
          </div>
        )}
        {phase === 'countdown' && count === 0 && (
          <div className="text-4xl font-bold text-orange-400 animate-pulse">
            🚀 LIFTOFF!
          </div>
        )}
        {phase === 'flying' && (
          <div className="mt-40 text-center animate-fade-in">
            <h1 className="text-3xl font-bold text-white mb-2">Welcome to CareerPath AI</h1>
            <p className="text-indigo-300">Launching your career to new heights...</p>
          </div>
        )}
      </div>

      {/* Ground */}
      {phase === 'countdown' && (
        <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-slate-800 to-transparent" />
      )}
    </div>
  );
};

// Custom Logo Component
const Logo = ({ size = 40 }: { size?: number }) => (
  <svg width={size} height={size} viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="rocketGradientDash" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#6366F1" />
        <stop offset="50%" stopColor="#8B5CF6" />
        <stop offset="100%" stopColor="#A855F7" />
      </linearGradient>
      <linearGradient id="flameGradientDash" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stopColor="#FBBF24" />
        <stop offset="50%" stopColor="#F97316" />
        <stop offset="100%" stopColor="#EF4444" />
      </linearGradient>
      <linearGradient id="windowGradientDash" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#38BDF8" />
        <stop offset="100%" stopColor="#0EA5E9" />
      </linearGradient>
    </defs>
    
    <circle cx="28" cy="28" r="26" fill="url(#rocketGradientDash)" opacity="0.1"/>
    <path d="M28 8C28 8 38 18 38 30C38 38 34 44 28 46C22 44 18 38 18 30C18 18 28 8 28 8Z" 
          fill="url(#rocketGradientDash)" />
    <circle cx="28" cy="24" r="6" fill="url(#windowGradientDash)" />
    <circle cx="28" cy="24" r="4" fill="#1E293B" />
    <circle cx="26" cy="22" r="1.5" fill="#38BDF8" opacity="0.6" />
    <path d="M18 34L12 42L18 40V34Z" fill="url(#rocketGradientDash)" />
    <path d="M38 34L44 42L38 40V34Z" fill="url(#rocketGradientDash)" />
    <ellipse cx="28" cy="50" rx="6" ry="4" fill="url(#flameGradientDash)" />
    <ellipse cx="28" cy="49" rx="4" ry="3" fill="#FBBF24" />
    <ellipse cx="28" cy="48" rx="2" ry="2" fill="#FEF3C7" />
  </svg>
);

// Skills Modal Component
const SkillsModal = ({ 
  isOpen, 
  onClose, 
  selectedSkills, 
  onToggleSkill,
  onRemoveSkill,
  customSkill,
  setCustomSkill,
  onAddCustomSkill
}: {
  isOpen: boolean;
  onClose: () => void;
  selectedSkills: string[];
  onToggleSkill: (skill: string) => void;
  onRemoveSkill: (skill: string) => void;
  customSkill: string;
  setCustomSkill: (skill: string) => void;
  onAddCustomSkill: () => void;
}) => {
  if (!isOpen) return null;

  // Get custom skills (skills not in the original options)
  const customSkills = selectedSkills.filter(skill => !SKILLS_OPTIONS.includes(skill));

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-4 max-h-[80vh] flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Select Your Skills</h2>
          <button 
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-lg transition-all"
          >
            <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Skills Grid */}
        <div className="p-4 overflow-y-auto flex-1">
          <p className="text-sm text-gray-600 mb-3">Click to select/deselect skills:</p>
          <div className="flex flex-wrap gap-2">
            {SKILLS_OPTIONS.map((skill) => (
              <button
                key={skill}
                onClick={() => onToggleSkill(skill)}
                className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all ${
                  selectedSkills.includes(skill)
                    ? "bg-indigo-600 text-white shadow-md"
                    : "bg-gray-100 text-gray-900 hover:bg-gray-200 border border-gray-300"
                }`}
              >
                {selectedSkills.includes(skill) && (
                  <span className="mr-1">✓</span>
                )}
                {skill}
              </button>
            ))}
          </div>

          {/* Custom Skills Section */}
          {customSkills.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-600 mb-2">Your custom skills:</p>
              <div className="flex flex-wrap gap-2">
                {customSkills.map((skill) => (
                  <button
                    key={skill}
                    onClick={() => onRemoveSkill(skill)}
                    className="px-3 py-1.5 rounded-full text-sm font-medium bg-purple-600 text-white shadow-md flex items-center gap-1 hover:bg-purple-700 transition-all"
                  >
                    {skill}
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Custom Skill Input */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-2">Add custom skill:</p>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Enter skill name..."
                value={customSkill}
                onChange={(e) => setCustomSkill(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && onAddCustomSkill()}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                onClick={onAddCustomSkill}
                disabled={!customSkill.trim()}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-indigo-700 transition-all"
              >
                Add
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 flex items-center justify-between">
          <p className="text-sm text-gray-600">
            {selectedSkills.length} skill{selectedSkills.length !== 1 ? 's' : ''} selected
          </p>
          <button
            onClick={onClose}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-all"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};

export default function Dashboard({ user }: DashboardProps) {
  const [showLaunchAnimation, setShowLaunchAnimation] = useState(true);
  const [targetRole, setTargetRole] = useState("");
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [customSkill, setCustomSkill] = useState("");
  const [timeframe, setTimeframe] = useState(6);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("recommendation");
  const [showSettings, setShowSettings] = useState(false);
  const [showSkillsModal, setShowSkillsModal] = useState(false);
  const [recentChats, setRecentChats] = useState([
    { id: 1, title: "Senior GenAI Engineer" },
    { id: 2, title: "ML Engineer Analysis" },
  ]);
  const [hoveredChat, setHoveredChat] = useState<number | null>(null);

  // Check if user has visited before
  useEffect(() => {
    const hasVisited = localStorage.getItem('careerpath_visited');
    if (hasVisited) {
      setShowLaunchAnimation(false);
    }
  }, []);

  const handleAnimationComplete = () => {
    localStorage.setItem('careerpath_visited', 'true');
    setShowLaunchAnimation(false);
  };

  const userName = user.user_metadata?.full_name || user.user_metadata?.name || user.email?.split("@")[0];
  const avatarUrl = user.user_metadata?.avatar_url;

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  const toggleSkill = (skill: string) => {
    setSelectedSkills((prev) =>
      prev.includes(skill)
        ? prev.filter((s) => s !== skill)
        : [...prev, skill]
    );
  };

  const removeSkill = (skill: string) => {
    setSelectedSkills((prev) => prev.filter((s) => s !== skill));
  };

  const handleAddCustomSkill = () => {
    if (customSkill.trim() && !selectedSkills.includes(customSkill.trim())) {
      setSelectedSkills([...selectedSkills, customSkill.trim()]);
      setCustomSkill("");
    }
  };

  const handleDeleteChat = (id: number) => {
    setRecentChats(recentChats.filter(chat => chat.id !== id));
  };

  const handleAnalysis = async () => {
    if (!targetRole.trim()) return;
    
    setLoading(true);
    setResults(null);

    // Add to recent chats
    const newChat = { id: Date.now(), title: targetRole };
    setRecentChats([newChat, ...recentChats.slice(0, 9)]);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: user.id,
          target_role: targetRole,
          current_skills: selectedSkills,
          timeframe_months: timeframe,
        }),
      });

      if (!response.ok) throw new Error("Analysis failed");
      
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Error:", error);
      // Mock results for demo
      setResults({
        final_recommendations: `Based on your skills in ${selectedSkills.join(", ") || "your current expertise"}, you're well-positioned for a ${targetRole} role.\n\n**Key Recommendations:**\n\n1. **Strengthen Core Skills** - Focus on deepening your knowledge in AI/ML frameworks\n2. **Build Portfolio Projects** - Create 2-3 production-ready projects showcasing your abilities\n3. **Network Strategically** - Connect with professionals in your target companies\n4. **Get Certified** - Consider Azure AI or AWS ML certifications`,
        market_research: `**Market Overview for ${targetRole}:**\n\n• **Demand:** High and growing rapidly\n• **Average Salary:** $150,000 - $200,000\n• **Top Hiring Companies:** Microsoft, Google, OpenAI, Anthropic\n• **Key Trends:** LLM applications, AI agents, RAG systems\n\n**Skills in Highest Demand:**\n- Python, LangChain, Semantic Kernel\n- Azure OpenAI, AWS Bedrock\n- Vector databases, RAG architectures`,
        learning_plan: `**${timeframe}-Month Learning Plan:**\n\n**Month 1-2:** Foundation\n• Complete Azure AI Fundamentals\n• Build first LLM-powered project\n\n**Month 3-4:** Advanced Skills\n• Master Semantic Kernel/LangChain\n• Implement RAG systems\n\n**Month 5-${timeframe}:** Portfolio & Applications\n• Create 2 production projects\n• Contribute to open source\n• Start applying to target companies`,
        application_strategy: `**Application Strategy:**\n\n1. **Target Companies:** Focus on mid-size tech companies and AI startups initially\n\n2. **Resume Optimization:**\n   - Highlight AI/ML projects\n   - Quantify your impact\n   - Include GitHub links\n\n3. **Interview Prep:**\n   - Practice system design for AI\n   - Prepare project deep-dives\n   - Study ML fundamentals\n\n4. **Networking:**\n   - Attend AI meetups\n   - Engage on LinkedIn\n   - Reach out to hiring managers`
      });
    } finally {
      setLoading(false);
    }
  };

  // Show launch animation on first visit
  if (showLaunchAnimation) {
    return <RocketLaunchAnimation onComplete={handleAnimationComplete} />;
  }

  return (
    <div className="min-h-screen bg-white flex">
      {/* Skills Modal */}
      <SkillsModal
        isOpen={showSkillsModal}
        onClose={() => setShowSkillsModal(false)}
        selectedSkills={selectedSkills}
        onToggleSkill={toggleSkill}
        onRemoveSkill={removeSkill}
        customSkill={customSkill}
        setCustomSkill={setCustomSkill}
        onAddCustomSkill={handleAddCustomSkill}
      />

      {/* Sidebar */}
      <div className="w-64 bg-gray-50 border-r border-gray-200 flex flex-col">
        {/* Logo */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <Logo size={36} />
            <span className="font-semibold text-gray-800">CareerPath AI</span>
          </div>
        </div>

        {/* New Chat Button */}
        <div className="p-3">
          <button 
            onClick={() => { setResults(null); setTargetRole(""); setSelectedSkills([]); }}
            className="w-full flex items-center gap-2 px-3 py-2.5 text-gray-700 hover:bg-gray-200 rounded-lg transition-all border border-gray-300"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Analysis
          </button>
        </div>

        {/* History Section */}
        <div className="flex-1 overflow-y-auto px-3 py-2">
          <p className="text-xs text-gray-500 px-2 mb-2">Recent</p>
          <div className="space-y-1">
            {recentChats.map((chat) => (
              <div
                key={chat.id}
                className="relative group"
                onMouseEnter={() => setHoveredChat(chat.id)}
                onMouseLeave={() => setHoveredChat(null)}
              >
                <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-200 rounded-lg truncate pr-8">
                  {chat.title}
                </button>
                {hoveredChat === chat.id && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteChat(chat.id);
                    }}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-red-100 rounded transition-all"
                    title="Delete"
                  >
                    <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                )}
              </div>
            ))}
            {recentChats.length === 0 && (
              <p className="text-xs text-gray-400 px-3 py-2">No recent analyses</p>
            )}
          </div>
        </div>

        {/* User Section */}
        <div className="p-3 border-t border-gray-200">
          <button 
            onClick={() => setShowSettings(!showSettings)}
            className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-200 rounded-lg transition-all"
          >
            {avatarUrl ? (
              <img src={avatarUrl} alt="Avatar" className="w-8 h-8 rounded-full" />
            ) : (
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center text-white text-sm font-medium">
                {userName?.charAt(0).toUpperCase()}
              </div>
            )}
            <span className="text-sm text-gray-700 truncate flex-1 text-left">{userName}</span>
            <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
            </svg>
          </button>
          
          {showSettings && (
            <div className="mt-2 py-1 bg-white rounded-lg shadow-lg border border-gray-200">
              <button 
                onClick={() => {
                  localStorage.removeItem('careerpath_visited');
                  setShowLaunchAnimation(true);
                  setShowSettings(false);
                }}
                className="w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 text-left flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Replay Animation
              </button>
              <button className="w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 text-left flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Settings
              </button>
              <button 
                onClick={handleLogout}
                className="w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 text-left flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Log out
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Main Area */}
        <div className="flex-1 overflow-y-auto">
          {!results ? (
            /* Empty State - Like ChatGPT */
            <div className="h-full flex flex-col items-center justify-center px-4">
              <Logo size={64} />
              <h1 className="mt-6 text-2xl font-semibold text-gray-800">How can I help with your career today?</h1>
              <p className="mt-2 text-gray-500 text-center max-w-md">
                Tell me about your target role and I'll provide personalized career analysis, market insights, and a learning plan.
              </p>

              {/* Quick Suggestions */}
              <div className="mt-8 grid grid-cols-2 gap-3 max-w-2xl w-full">
                {[
                  { title: "Analyze career path", subtitle: "for Senior GenAI Engineer" },
                  { title: "Create learning plan", subtitle: "for Machine Learning role" },
                  { title: "Market research", subtitle: "for AI/ML positions" },
                  { title: "Application strategy", subtitle: "for tech companies" },
                ].map((suggestion, i) => (
                  <button
                    key={i}
                    onClick={() => setTargetRole(suggestion.subtitle.replace("for ", ""))}
                    className="p-4 text-left border border-gray-200 rounded-xl hover:bg-gray-50 transition-all group"
                  >
                    <p className="font-medium text-gray-800 group-hover:text-indigo-600">{suggestion.title}</p>
                    <p className="text-sm text-gray-500">{suggestion.subtitle}</p>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            /* Results Display */
            <div className="max-w-3xl mx-auto py-8 px-4">
              {/* User Query */}
              <div className="flex gap-4 mb-8">
                {avatarUrl ? (
                  <img src={avatarUrl} alt="Avatar" className="w-8 h-8 rounded-full" />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center text-white text-sm font-medium">
                    {userName?.charAt(0).toUpperCase()}
                  </div>
                )}
                <div>
                  <p className="font-medium text-gray-800">Analyze career path for: {targetRole}</p>
                  <p className="text-sm text-gray-500">Skills: {selectedSkills.join(", ") || "Not specified"} • Timeline: {timeframe} months</p>
                </div>
              </div>

              {/* AI Response */}
              <div className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center flex-shrink-0">
                  <Logo size={20} />
                </div>
                <div className="flex-1">
                  {/* Tabs */}
                  <div className="flex gap-1 mb-4 border-b border-gray-200">
                    {[
                      { id: "recommendation", label: "Summary" },
                      { id: "market", label: "Market" },
                      { id: "learning", label: "Learning" },
                      { id: "strategy", label: "Strategy" },
                    ].map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2 text-sm font-medium transition-all border-b-2 -mb-px ${
                          activeTab === tab.id
                            ? "border-indigo-600 text-indigo-600"
                            : "border-transparent text-gray-500 hover:text-gray-700"
                        }`}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>

                  {/* Tab Content */}
                  <div className="prose prose-gray max-w-none">
                    {activeTab === "recommendation" && (
                      <div className="text-gray-700 whitespace-pre-line leading-relaxed">
                        {results.final_recommendations}
                      </div>
                    )}
                    {activeTab === "market" && (
                      <div className="text-gray-700 whitespace-pre-line leading-relaxed">
                        {results.market_research}
                      </div>
                    )}
                    {activeTab === "learning" && (
                      <div className="text-gray-700 whitespace-pre-line leading-relaxed">
                        {results.learning_plan}
                      </div>
                    )}
                    {activeTab === "strategy" && (
                      <div className="text-gray-700 whitespace-pre-line leading-relaxed">
                        {results.application_strategy}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area - Fixed at bottom */}
        <div className="border-t border-gray-200 bg-white p-4">
          <div className="max-w-3xl mx-auto">
            {/* Selected Skills Display */}
            {selectedSkills.length > 0 && (
              <div className="mb-3 flex flex-wrap gap-2 items-center">
                <span className="text-xs text-gray-500">Your skills:</span>
                {selectedSkills.slice(0, 5).map((skill) => (
                  <span key={skill} className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs">
                    {skill}
                  </span>
                ))}
                {selectedSkills.length > 5 && (
                  <span className="text-xs text-gray-500">+{selectedSkills.length - 5} more</span>
                )}
                <button
                  onClick={() => setShowSkillsModal(true)}
                  className="text-xs text-indigo-600 hover:underline"
                >
                  Edit
                </button>
              </div>
            )}

            {/* Input Box */}
            <div className="relative flex items-center gap-2">
              {/* Skills Button with Label */}
              <button
                onClick={() => setShowSkillsModal(true)}
                className={`px-3 py-3 rounded-xl transition-all border flex items-center gap-2 ${
                  selectedSkills.length > 0 
                    ? "bg-indigo-50 border-indigo-200 text-indigo-600" 
                    : "bg-gray-100 border-gray-200 text-gray-600 hover:bg-gray-200"
                }`}
                title="Select your skills"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                <span className="text-sm font-medium whitespace-nowrap">
                  {selectedSkills.length > 0 ? `${selectedSkills.length} Skills` : "Add Skills"}
                </span>
              </button>

              {/* Text Input */}
              <div className="flex-1 relative">
                <input
                  type="text"
                  placeholder="Enter your target role (e.g., Senior GenAI Engineer)..."
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAnalysis()}
                  className="w-full px-4 py-3 pr-24 bg-gray-100 border border-gray-200 rounded-2xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-white transition-all"
                />
                <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
                  <select
                    value={timeframe}
                    onChange={(e) => setTimeframe(parseInt(e.target.value))}
                    className="text-xs bg-transparent text-gray-500 focus:outline-none cursor-pointer"
                  >
                    {[3, 6, 9, 12].map((m) => (
                      <option key={m} value={m}>{m}mo</option>
                    ))}
                  </select>
                  <button
                    onClick={handleAnalysis}
                    disabled={loading || !targetRole.trim()}
                    className="p-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white rounded-xl transition-all disabled:cursor-not-allowed"
                  >
                    {loading ? (
                      <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            </div>
            <p className="mt-2 text-xs text-center text-gray-400">
              CareerPath AI provides career guidance based on market data and AI analysis.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
