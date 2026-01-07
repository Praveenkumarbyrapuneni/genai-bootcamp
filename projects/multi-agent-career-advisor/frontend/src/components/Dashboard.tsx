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

// Timeframe Picker Component
const TimeframePicker = ({
  isOpen,
  onClose,
  timeframeValue,
  timeframeUnit,
  onSave
}: {
  isOpen: boolean;
  onClose: () => void;
  timeframeValue: number;
  timeframeUnit: 'days' | 'months' | 'years';
  onSave: (value: number, unit: 'days' | 'months' | 'years') => void;
}) => {
  const [localValue, setLocalValue] = useState(timeframeValue);
  const [localUnit, setLocalUnit] = useState<'days' | 'months' | 'years'>(timeframeUnit);

  useEffect(() => {
    setLocalValue(timeframeValue);
    setLocalUnit(timeframeUnit);
  }, [timeframeValue, timeframeUnit, isOpen]);

  if (!isOpen) return null;

  const getMaxValue = () => {
    switch (localUnit) {
      case 'days': return 365;
      case 'months': return 24;
      case 'years': return 5;
      default: return 12;
    }
  };

  const getValueOptions = () => {
    const max = getMaxValue();
    return Array.from({ length: max }, (_, i) => i + 1);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm mx-4">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Set Goal Timeline</h2>
          <button 
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-lg transition-all"
          >
            <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Unit Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">Select time unit:</label>
            <div className="grid grid-cols-3 gap-2">
              {(['days', 'months', 'years'] as const).map((unit) => (
                <button
                  key={unit}
                  onClick={() => {
                    setLocalUnit(unit);
                    // Reset value when changing unit
                    if (unit === 'days') setLocalValue(Math.min(localValue, 30) || 30);
                    else if (unit === 'months') setLocalValue(Math.min(localValue, 6) || 6);
                    else setLocalValue(Math.min(localValue, 2) || 1);
                  }}
                  className={`px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                    localUnit === unit
                      ? "bg-indigo-600 text-white shadow-md"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {unit.charAt(0).toUpperCase() + unit.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Value Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Number of {localUnit}:
            </label>
            <div className="flex items-center gap-4">
              {/* Decrease Button */}
              <button
                onClick={() => setLocalValue(Math.max(1, localValue - 1))}
                disabled={localValue <= 1}
                className="w-12 h-12 rounded-xl bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-all"
              >
                <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
                </svg>
              </button>

              {/* Value Display */}
              <div className="flex-1">
                <select
                  value={localValue}
                  onChange={(e) => setLocalValue(parseInt(e.target.value))}
                  className="w-full text-center text-3xl font-bold text-indigo-600 bg-indigo-50 border-2 border-indigo-200 rounded-xl py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
                >
                  {getValueOptions().map((val) => (
                    <option key={val} value={val}>{val}</option>
                  ))}
                </select>
              </div>

              {/* Increase Button */}
              <button
                onClick={() => setLocalValue(Math.min(getMaxValue(), localValue + 1))}
                disabled={localValue >= getMaxValue()}
                className="w-12 h-12 rounded-xl bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-all"
              >
                <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              </button>
            </div>
          </div>

          {/* Preview */}
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 mb-6">
            <p className="text-sm text-gray-600 text-center">Your goal timeline:</p>
            <p className="text-2xl font-bold text-center text-indigo-600 mt-1">
              {localValue} {localValue === 1 ? localUnit.slice(0, -1) : localUnit}
            </p>
          </div>

          {/* Quick Select */}
          <div className="mb-4">
            <label className="block text-xs text-gray-500 mb-2">Quick select:</label>
            <div className="flex flex-wrap gap-2">
              {[
                { value: 30, unit: 'days' as const, label: '30 Days' },
                { value: 3, unit: 'months' as const, label: '3 Months' },
                { value: 6, unit: 'months' as const, label: '6 Months' },
                { value: 1, unit: 'years' as const, label: '1 Year' },
                { value: 2, unit: 'years' as const, label: '2 Years' },
              ].map((preset) => (
                <button
                  key={preset.label}
                  onClick={() => {
                    setLocalValue(preset.value);
                    setLocalUnit(preset.unit);
                  }}
                  className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                    localValue === preset.value && localUnit === preset.unit
                      ? "bg-indigo-600 text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2.5 bg-gray-100 text-gray-700 rounded-xl font-medium hover:bg-gray-200 transition-all"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onSave(localValue, localUnit);
              onClose();
            }}
            className="flex-1 px-4 py-2.5 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 transition-all"
          >
            Apply
          </button>
        </div>
      </div>
    </div>
  );
};

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
  const [timeframeValue, setTimeframeValue] = useState(6);
  const [timeframeUnit, setTimeframeUnit] = useState<'days' | 'months' | 'years'>('months');
  const [showTimeframePicker, setShowTimeframePicker] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("recommendation");
  const [showSettings, setShowSettings] = useState(false);
  const [showSkillsModal, setShowSkillsModal] = useState(false);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState<string>("");
  const [resumeSkills, setResumeSkills] = useState<string[]>([]);
  const [parsingResume, setParsingResume] = useState(false);
  const [recentChats, setRecentChats] = useState<{id: number, title: string, results?: any}[]>([]);
  const [hoveredChat, setHoveredChat] = useState<number | null>(null);
  const [currentChatId, setCurrentChatId] = useState<number | null>(null);

  // Helper function to get timeframe display text
  const getTimeframeDisplay = () => {
    const unitLabel = timeframeValue === 1 ? timeframeUnit.slice(0, -1) : timeframeUnit;
    return `${timeframeValue} ${unitLabel}`;
  };

  // Helper function to convert timeframe to months for API
  const getTimeframeInMonths = () => {
    switch (timeframeUnit) {
      case 'days': return Math.max(1, Math.ceil(timeframeValue / 30));
      case 'months': return timeframeValue;
      case 'years': return timeframeValue * 12;
      default: return timeframeValue;
    }
  };

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
    if (currentChatId === id) {
      handleNewChat();
    }
  };

  const handleNewChat = () => {
    setResults(null);
    setTargetRole("");
    setSelectedSkills([]);
    setResumeFile(null);
    setResumeText("");
    setResumeSkills([]);
    setCurrentChatId(null);
    setActiveTab("recommendation");
  };

  const handleSelectChat = (chat: {id: number, title: string, results?: any}) => {
    if (chat.results) {
      setResults(chat.results);
      setTargetRole(chat.title);
      setCurrentChatId(chat.id);
    }
  };

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setResumeFile(file);
    setParsingResume(true);
    
    // Try to parse the resume
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/parse-resume`, {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const data = await response.json();
        setResumeText(data.text);
        
        // Auto-add extracted skills to selected skills
        if (data.extracted_skills && data.extracted_skills.length > 0) {
          setResumeSkills(data.extracted_skills);
          // Merge with existing skills (avoid duplicates)
          setSelectedSkills(prev => {
            const combined = [...prev];
            data.extracted_skills.forEach((skill: string) => {
              if (!combined.some(s => s.toLowerCase() === skill.toLowerCase())) {
                combined.push(skill);
              }
            });
            return combined;
          });
        }
      } else {
        // If API fails, try to read as text and extract skills locally
        if (file.type === 'text/plain') {
          const text = await file.text();
          setResumeText(text);
          const skills = extractSkillsLocally(text);
          if (skills.length > 0) {
            setResumeSkills(skills);
            setSelectedSkills(prev => {
              const combined = [...prev];
              skills.forEach((skill: string) => {
                if (!combined.some(s => s.toLowerCase() === skill.toLowerCase())) {
                  combined.push(skill);
                }
              });
              return combined;
            });
          }
        }
      }
    } catch (error) {
      console.error("Resume parsing error:", error);
      // If API fails, try to read as text
      if (file.type === 'text/plain') {
        const text = await file.text();
        setResumeText(text);
        const skills = extractSkillsLocally(text);
        if (skills.length > 0) {
          setResumeSkills(skills);
          setSelectedSkills(prev => {
            const combined = [...prev];
            skills.forEach((skill: string) => {
              if (!combined.some(s => s.toLowerCase() === skill.toLowerCase())) {
                combined.push(skill);
              }
            });
            return combined;
          });
        }
      }
    } finally {
      setParsingResume(false);
    }
  };

  // Local skill extraction fallback
  const extractSkillsLocally = (text: string): string[] => {
    const allSkills = [
      "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby", "PHP",
      "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI", "Spring",
      "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis",
      "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
      "Data Analysis", "Data Science", "Data Visualization", "Tableau", "Power BI", "Excel", "Statistics",
      "NLP", "Computer Vision",
      "LLM", "OpenAI", "Azure OpenAI", "Prompt Engineering", "RAG", "LangChain", "Semantic Kernel",
      "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions",
      "Git", "Agile", "Scrum", "System Design", "Microservices",
      "ETL", "A/B Testing", "Data Structures", "Algorithms"
    ];
    
    const textLower = text.toLowerCase();
    return allSkills.filter(skill => textLower.includes(skill.toLowerCase()));
  };

  // Deep resume analysis for fallback (when API is unavailable)
  const analyzeResumeLocally = (resumeText: string, targetRole: string, timeframe: string) => {
    const textLower = resumeText.toLowerCase();
    
    // Extract experience info
    const experiencePatterns = [
      /(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)/i,
      /(experience|worked)\s*(at|for|with)\s*([A-Za-z\s]+)/gi,
      /(software|data|ml|ai|frontend|backend|full\s*stack)\s*(engineer|developer|analyst|scientist)/gi,
    ];
    
    let yearsOfExp = 0;
    const expMatch = resumeText.match(/(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)/i);
    if (expMatch) yearsOfExp = parseInt(expMatch[1]);
    
    // Extract companies
    const companies: string[] = [];
    const companyPatterns = ["google", "microsoft", "amazon", "meta", "facebook", "apple", "netflix", 
      "uber", "airbnb", "stripe", "linkedin", "twitter", "oracle", "salesforce", "adobe", 
      "ibm", "intel", "nvidia", "tcs", "infosys", "wipro", "cognizant", "accenture"];
    companyPatterns.forEach(company => {
      if (textLower.includes(company)) companies.push(company.charAt(0).toUpperCase() + company.slice(1));
    });
    
    // Extract projects
    const hasProjects = textLower.includes("project") || textLower.includes("built") || textLower.includes("developed");
    const projectCount = (resumeText.match(/project/gi) || []).length;
    
    // Extract education
    const hasMasters = textLower.includes("master") || textLower.includes("m.s.") || textLower.includes("mtech") || textLower.includes("m.tech");
    const hasBachelors = textLower.includes("bachelor") || textLower.includes("b.s.") || textLower.includes("btech") || textLower.includes("b.tech") || textLower.includes("b.e.");
    const hasPhD = textLower.includes("phd") || textLower.includes("doctorate");
    
    // Extract certifications
    const certKeywords = ["certified", "certification", "certificate", "aws certified", "azure certified", "google certified"];
    const hasCerts = certKeywords.some(cert => textLower.includes(cert));
    
    // Calculate readiness based on resume content
    let resumeScore = 0;
    if (yearsOfExp >= 3) resumeScore += 25;
    else if (yearsOfExp >= 1) resumeScore += 15;
    else resumeScore += 5;
    
    if (companies.length > 0) resumeScore += 20;
    if (projectCount >= 3) resumeScore += 20;
    else if (projectCount >= 1) resumeScore += 10;
    
    if (hasPhD) resumeScore += 15;
    else if (hasMasters) resumeScore += 10;
    else if (hasBachelors) resumeScore += 5;
    
    if (hasCerts) resumeScore += 10;
    
    // Skills match
    const extractedSkills = extractSkillsLocally(resumeText);
    resumeScore += Math.min(20, extractedSkills.length * 2);
    
    resumeScore = Math.min(100, resumeScore);
    
    return {
      yearsOfExp,
      companies,
      projectCount,
      hasProjects,
      hasMasters,
      hasBachelors,
      hasPhD,
      hasCerts,
      extractedSkills,
      resumeScore,
      education: hasPhD ? "PhD" : hasMasters ? "Master's" : hasBachelors ? "Bachelor's" : "Not specified"
    };
  };

  // Generate deep resume-based mock results
  const generateResumeBasedMockResults = (
    resumeText: string, 
    targetRole: string, 
    timeframe: string,
    requiredSkills: string[],
    selectedSkills: string[]
  ) => {
    const analysis = analyzeResumeLocally(resumeText, targetRole, timeframe);
    
    const currentLower = selectedSkills.map(s => s.toLowerCase());
    const matchedSkills = requiredSkills.filter(skill => 
      currentLower.some(curr => curr.includes(skill.toLowerCase()) || skill.toLowerCase().includes(curr))
    );
    const missingSkills = requiredSkills.filter(skill => 
      !currentLower.some(curr => curr.includes(skill.toLowerCase()) || skill.toLowerCase().includes(curr))
    );
    
    return {
      final_recommendations: `## 🔍 DEEP RESUME ANALYSIS for ${targetRole}

### 📋 What I Found in Your Resume:

**Work Experience:**
${analysis.yearsOfExp > 0 ? `- ${analysis.yearsOfExp}+ years of experience detected` : "- ⚠️ No clear years of experience mentioned"}
${analysis.companies.length > 0 ? `- Companies: ${analysis.companies.join(", ")}` : "- No recognizable company names found"}
${analysis.companies.some(c => ["Google", "Microsoft", "Amazon", "Meta", "Apple"].includes(c)) ? "- ✅ FAANG/Big Tech experience - this is a big plus!" : ""}

**Projects:**
${analysis.projectCount > 0 ? `- Found ~${analysis.projectCount} project mentions` : "- ⚠️ No projects clearly mentioned"}
${analysis.hasProjects ? "- You have project experience" : "- ❌ Add more project descriptions to your resume"}

**Education:**
- ${analysis.education} degree
${analysis.hasPhD ? "✅ PhD is excellent for research-focused roles" : ""}
${analysis.hasMasters ? "✅ Master's degree is a plus" : ""}

**Skills Detected:**
${analysis.extractedSkills.length > 0 ? analysis.extractedSkills.slice(0, 10).map(s => `- ${s}`).join('\n') : "- No technical skills clearly mentioned"}

---

## 🚨 REALITY CHECK

### Your Resume-Based Readiness: ${analysis.resumeScore}%
${analysis.resumeScore < 40 ? "⚠️ Your resume needs significant improvement for " + targetRole :
  analysis.resumeScore < 60 ? "🔶 Your resume shows potential but has gaps for " + targetRole :
  analysis.resumeScore < 80 ? "✅ Your resume is decent for " + targetRole + " but could be stronger" :
  "✅ Your resume is strong for " + targetRole}

### ✅ Resume Strengths:
${analysis.yearsOfExp >= 2 ? `- ${analysis.yearsOfExp}+ years of experience` : ""}
${analysis.companies.length > 0 ? `- Experience at ${analysis.companies.join(", ")}` : ""}
${analysis.projectCount >= 2 ? `- Multiple projects mentioned` : ""}
${analysis.hasCerts ? "- Has relevant certifications" : ""}
${analysis.extractedSkills.length >= 5 ? `- Good skill coverage (${analysis.extractedSkills.length} skills found)` : ""}
${analysis.yearsOfExp < 1 && analysis.projectCount < 2 && analysis.extractedSkills.length < 3 ? "- ❌ Very few strengths detected - resume needs major work" : ""}

### ❌ Resume Weaknesses:
${analysis.yearsOfExp < 2 ? "- Limited professional experience" : ""}
${analysis.companies.length === 0 ? "- No recognizable company names (affects credibility)" : ""}
${analysis.projectCount < 2 ? "- Too few projects mentioned" : ""}
${!analysis.hasCerts ? "- No certifications mentioned" : ""}
${missingSkills.length > 0 ? `- Missing key skills: ${missingSkills.slice(0, 5).join(", ")}` : ""}

### 🎯 Experience Gap for ${targetRole}:
${analysis.yearsOfExp < 1 ? 
  `Most ${targetRole} positions want 1-2+ years of experience. You appear to be entry-level.` :
  analysis.yearsOfExp < 3 ?
  `You have ${analysis.yearsOfExp}+ years - competitive for junior to mid-level ${targetRole} roles.` :
  `${analysis.yearsOfExp}+ years puts you in the mid to senior range for ${targetRole}.`}

### 📊 Projects Assessment:
${analysis.projectCount === 0 ? 
  `❌ **CRITICAL**: No projects visible in your resume. For ${targetRole}, you NEED 2-3 solid projects.` :
  analysis.projectCount < 3 ?
  `⚠️ You have ~${analysis.projectCount} project(s). Add ${3 - analysis.projectCount} more relevant projects for ${targetRole}.` :
  `✅ Good project count. Make sure they're relevant to ${targetRole}.`}

### ⏰ Is ${timeframe} Realistic?
${analysis.resumeScore >= 70 ? 
  `With your resume, ${timeframe} is reasonable to start applying.` :
  analysis.resumeScore >= 50 ?
  `${timeframe} is tight. Focus on filling the gaps I mentioned above.` :
  `${timeframe} may not be enough. Your resume needs significant improvement first.`}

### 📋 Priority Actions:
1. ${missingSkills.length > 0 ? `Add ${missingSkills[0]} to your skillset and resume` : "Polish your existing skills section"}
2. ${analysis.projectCount < 3 ? `Build ${3 - analysis.projectCount} more projects for ${targetRole}` : "Make sure projects show quantified impact"}
3. ${analysis.yearsOfExp < 2 ? "Get more hands-on experience (internships, freelance, or personal projects)" : "Quantify achievements with numbers (%, $, users)"}
4. ${!analysis.hasCerts ? `Get a relevant certification for ${targetRole}` : "Highlight your certifications more prominently"}
5. ${analysis.companies.length === 0 ? "Consider internships at known companies for credibility" : "Leverage your company experience in interviews"}

### 💡 Bottom Line:
${analysis.resumeScore < 40 ?
  `Your resume is at ${analysis.resumeScore}% readiness. This is honest: you're not ready for ${targetRole} yet. Focus on building projects, learning ${missingSkills.slice(0, 2).join(" and ")}, and getting more experience before applying.` :
  analysis.resumeScore < 60 ?
  `At ${analysis.resumeScore}%, you have a foundation but significant gaps. You might get callbacks from smaller companies, but top companies will pass. Fill the gaps I mentioned.` :
  analysis.resumeScore < 80 ?
  `${analysis.resumeScore}% readiness - you're in a reasonable position. Start applying while addressing the weaknesses I pointed out.` :
  `Strong resume at ${analysis.resumeScore}%. You should be competitive for ${targetRole} positions. Focus on interview prep.`}`,

      market_research: `## 📊 Market Fit Analysis for ${targetRole}

### How Your Resume Compares:

| Requirement | Typical Ask | Your Resume | Status |
|-------------|-------------|-------------|--------|
| Experience | 2-5 years | ${analysis.yearsOfExp}+ years | ${analysis.yearsOfExp >= 2 ? "✅" : "⚠️"} |
| Projects | 2-3 relevant | ~${analysis.projectCount} found | ${analysis.projectCount >= 2 ? "✅" : "⚠️"} |
| Education | Bachelor's+ | ${analysis.education} | ${analysis.hasBachelors || analysis.hasMasters || analysis.hasPhD ? "✅" : "⚠️"} |
| Key Skills | ${requiredSkills.slice(0, 3).join(", ")} | ${matchedSkills.length}/${requiredSkills.length} | ${matchedSkills.length >= requiredSkills.length / 2 ? "✅" : "⚠️"} |

### Companies You Could Target:
Based on your resume:

**FAANG/Big Tech (Google, Meta, etc.):**
${analysis.resumeScore >= 75 && analysis.yearsOfExp >= 3 ? "✅ You could be competitive" : "⚠️ Not ready yet - need stronger experience/projects"}

**Mid-size Tech (Stripe, Airbnb, etc.):**
${analysis.resumeScore >= 60 && analysis.yearsOfExp >= 2 ? "✅ Worth applying" : "⚠️ Build more experience first"}

**Startups:**
${analysis.resumeScore >= 40 ? "✅ Good fit - startups value potential" : "🔶 Possible, but strengthen your resume"}

**Traditional Companies:**
${analysis.hasBachelors || analysis.hasMasters ? "✅ Usually less competitive" : "🔶 Degree might be required"}

### Skills From Your Resume vs Required:
**You have:** ${matchedSkills.length > 0 ? matchedSkills.join(", ") : "None of the core skills"}
**You need:** ${missingSkills.length > 0 ? missingSkills.join(", ") : "All core skills covered!"}

### Salary Expectations (Based on Your Profile):
${analysis.yearsOfExp < 2 ? 
  `Entry Level: $60,000 - $85,000` :
  analysis.yearsOfExp < 5 ?
  `Mid Level: $85,000 - $130,000` :
  `Senior Level: $130,000 - $200,000+`}

### Your Competitive Position:
${analysis.resumeScore < 40 ? "Bottom 25% of applicants" :
  analysis.resumeScore < 60 ? "Average applicant pool" :
  analysis.resumeScore < 80 ? "Top 50% of applicants" :
  "Top 25% of applicants"}`,

      learning_plan: `## 📚 Personalized Learning Plan

### Based on Your Resume:
I found these skills: ${analysis.extractedSkills.slice(0, 8).join(", ") || "No clear skills detected"}

### Skills You Need to Add:
${missingSkills.length > 0 ? missingSkills.map((skill, i) => `
#### ${i + 1}. ${skill}
- **Why:** Required for most ${targetRole} positions
- **Time to learn:** ${skill.toLowerCase().includes("sql") ? "2-3 weeks" : 
                       skill.toLowerCase().includes("python") ? "4-6 weeks" :
                       skill.toLowerCase().includes("machine") ? "8-12 weeks" : "3-4 weeks"}
- **Best resource:** ${skill.toLowerCase().includes("sql") ? "SQLZoo, Mode Analytics" :
                       skill.toLowerCase().includes("python") ? "Python for Everybody (Coursera)" :
                       "YouTube + hands-on projects"}
- **How to prove:** Add a project using ${skill} to your resume`).join('\n') :
"All required skills covered! Focus on deepening expertise."}

### Projects to Add to Your Resume:
${analysis.projectCount < 3 ? `
You need ${3 - analysis.projectCount} more projects. Build these:

1. **Data/Analysis Project:** Show you can work with real data
   - Example: Analyze a public dataset, create visualizations
   - Skills demonstrated: ${requiredSkills.slice(0, 2).join(", ")}

2. **End-to-End Project:** Show you can build complete solutions
   - Example: Build a complete application/pipeline
   - Skills demonstrated: System thinking, ${requiredSkills.slice(2, 4).join(", ")}

3. **Industry-Relevant Project:** Show domain knowledge
   - Example: Solve a real business problem
   - Skills demonstrated: Business acumen, technical skills` :
"Good project count! Make sure each has quantified impact (numbers, %, users)."}

### Experience Building:
${analysis.yearsOfExp < 2 ? `
Your experience is limited. Consider:
- Freelance projects on Upwork/Fiverr
- Open source contributions
- Internships (even part-time)
- Personal projects that simulate work experience` :
"Your experience level is good. Focus on quantifying achievements."}

### Timeline for ${timeframe}:
${analysis.resumeScore >= 60 ?
  `You can start applying now while improving. Dedicate 5-10 hours/week to filling gaps.` :
  `Focus ${timeframe} entirely on improvement before applying. You need 15-20 hours/week of work.`}`,

      application_strategy: `## 📝 Application Readiness

### Should You Apply Now?
${analysis.resumeScore >= 70 ? 
  "✅ **YES** - Your resume is competitive. Start applying." :
  analysis.resumeScore >= 50 ?
  "🔶 **SELECTIVELY** - Apply to mid-tier companies. Save top companies for later." :
  "⛔ **NOT YET** - Your resume needs work. Applying now = wasted applications."}

### Resume Fixes (Do These First):
${analysis.projectCount < 2 ? "1. ❌ Add 2-3 relevant projects with quantified results" : "1. ✅ Good project count"}
${missingSkills.length > 2 ? `2. ❌ Add missing skills: ${missingSkills.slice(0, 3).join(", ")}` : "2. ✅ Skills look reasonable"}
${analysis.yearsOfExp < 1 ? "3. ❌ Get more experience (internships, freelance)" : "3. ✅ Experience is adequate"}
4. Add quantified achievements (X% improvement, $X saved, X users)
5. Tailor resume for each application

### Interview Prep Based on Your Resume:
**Questions You'll Ace:**
${analysis.extractedSkills.slice(0, 3).map(s => `- Tell me about your experience with ${s}`).join('\n') || "- Generic background questions"}

**Questions You'll Struggle With:**
${missingSkills.slice(0, 3).map(s => `- How would you use ${s}? (You don't have it on resume)`).join('\n') || "- Deep technical dives on advanced topics"}

### Predicted Callback Rate:
- Current resume: ~${Math.round(analysis.resumeScore * 0.4)}% callback rate
- After improvements: ~${Math.round(Math.min(50, analysis.resumeScore * 0.6))}% callback rate

### Application Tier Strategy:
**Apply Now To:**
${analysis.resumeScore >= 50 ? "- Mid-size companies, startups" : "- Entry-level positions, smaller companies"}

**Wait 1-2 Months:**
${analysis.resumeScore >= 40 ? "- Larger tech companies" : "- Most tech companies"}

**Wait 3+ Months:**
${analysis.resumeScore >= 60 ? "- FAANG if that's your goal" : "- Any competitive company"}

### Your Priority Actions:
1. ${analysis.projectCount < 2 ? "Build 2 solid projects THIS MONTH" : "Add metrics to existing projects"}
2. ${missingSkills[0] ? `Learn ${missingSkills[0]} (most important gap)` : "Deepen expertise in your strongest skill"}
3. Get your resume reviewed by someone in the industry
4. Practice behavioral questions (STAR method)
5. ${analysis.yearsOfExp < 2 ? "Look for internships or junior roles" : "Network on LinkedIn with recruiters"}`
    };
  };

  const handleAnalysis = async () => {
    if (!targetRole.trim()) return;
    
    setLoading(true);
    setResults(null);

    const chatId = Date.now();
    setCurrentChatId(chatId);

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
          timeframe_months: getTimeframeInMonths(),
          timeframe_display: getTimeframeDisplay(),
          resume_text: resumeText || null,
        }),
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }
      
      const data = await response.json();
      setResults(data);
      
      // Add to recent chats with results
      const newChat = { id: chatId, title: targetRole, results: data };
      setRecentChats([newChat, ...recentChats.slice(0, 9)]);
      
    } catch (error) {
      console.error("Error:", error);
      alert("Unable to analyze. Please try again.");
      
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
            onClick={handleNewChat}
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
                <button 
                  onClick={() => handleSelectChat(chat)}
                  className={`w-full text-left px-3 py-2 text-sm rounded-lg truncate pr-8 transition-all ${
                    currentChatId === chat.id 
                      ? "bg-indigo-100 text-indigo-700" 
                      : "text-gray-700 hover:bg-gray-200"
                  }`}
                >
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
            /* Empty State */
            <div className="h-full flex flex-col items-center justify-center px-4">
              <Logo size={64} />
              <h1 className="mt-6 text-2xl font-semibold text-gray-800">Get Your Career Reality Check</h1>
              <p className="mt-2 text-gray-500 text-center max-w-md">
                No sugar-coating. Just honest feedback about your skills, gaps, and what you need to learn.
              </p>

              {/* Quick Suggestions */}
              <div className="mt-8 grid grid-cols-2 gap-3 max-w-2xl w-full">
                {[
                  { title: "Data Analyst", subtitle: "SQL, Excel, Tableau" },
                  { title: "Software Engineer", subtitle: "DSA, System Design" },
                  { title: "Data Scientist", subtitle: "ML, Python, Statistics" },
                  { title: "GenAI Engineer", subtitle: "LLMs, RAG, Prompting" },
                ].map((suggestion, i) => (
                  <button
                    key={i}
                    onClick={() => setTargetRole(suggestion.title)}
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
                  <p className="font-medium text-gray-800">Reality check for: {targetRole}</p>
                  <p className="text-sm text-gray-500">
                    Skills: {selectedSkills.join(", ") || "None specified"} • Timeline: {getTimeframeDisplay()}
                    {resumeFile && ` • Resume: ${resumeFile.name}`}
                  </p>
                </div>
              </div>

              {/* AI Response */}
              <div className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center flex-shrink-0">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div className="flex-1">
                  {/* Tabs */}
                  <div className="flex gap-1 mb-4 border-b border-gray-200 overflow-x-auto">
                    {[
                      { id: "recommendation", label: "Reality Check" },
                      { id: "market", label: "Market" },
                      { id: "learning", label: "Learning Plan" },
                      { id: "strategy", label: "Apply?" },
                    ].map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2 text-sm font-medium transition-all border-b-2 -mb-px whitespace-nowrap ${
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
            {/* Selected Skills & Resume Display */}
            {(selectedSkills.length > 0 || resumeFile) && (
              <div className="mb-3 flex flex-wrap gap-2 items-center">
                {resumeSkills.length > 0 && (
                  <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                    📄 {resumeSkills.length} skills from resume
                  </span>
                )}
                {selectedSkills.length > 0 && (
                  <>
                    <span className="text-xs text-gray-500">|</span>
                    {selectedSkills.slice(0, 5).map((skill) => (
                      <span 
                        key={skill} 
                        className={`px-2 py-1 rounded-full text-xs ${
                          resumeSkills.includes(skill) 
                            ? "bg-green-100 text-green-700" 
                            : "bg-indigo-100 text-indigo-700"
                        }`}
                      >
                        {skill}
                      </span>
                    ))}
                    {selectedSkills.length > 5 && (
                      <button 
                        onClick={() => setShowSkillsModal(true)}
                        className="text-xs text-indigo-600 hover:underline"
                      >
                        +{selectedSkills.length - 5} more
                      </button>
                    )}
                  </>
                )}
                {resumeFile && (
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs flex items-center gap-1">
                    {resumeFile.name}
                    <button 
                      onClick={() => { 
                        setResumeFile(null); 
                        setResumeText(""); 
                        // Remove resume-extracted skills
                        setSelectedSkills(prev => prev.filter(s => !resumeSkills.includes(s)));
                        setResumeSkills([]);
                      }} 
                      className="hover:text-red-500 ml-1"
                    >
                      ×
                    </button>
                  </span>
                )}
              </div>
            )}

            {/* Input Box */}
            <div className="relative flex items-center gap-2">
              {/* Skills Button */}
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
                  {selectedSkills.length > 0 ? `${selectedSkills.length} Skills` : "Skills"}
                </span>
              </button>

              {/* Timeframe Button */}
              <button
                onClick={() => setShowTimeframePicker(true)}
                className="px-3 py-3 rounded-xl transition-all border flex items-center gap-2 bg-purple-50 border-purple-200 text-purple-600 hover:bg-purple-100"
                title="Set goal timeline"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span className="text-sm font-medium whitespace-nowrap">
                  {getTimeframeDisplay()}
                </span>
              </button>

              {/* Resume Upload Button */}
              <label
                className={`px-3 py-3 rounded-xl transition-all border flex items-center gap-2 cursor-pointer ${
                  parsingResume 
                    ? "bg-yellow-50 border-yellow-200 text-yellow-600 animate-pulse"
                    : resumeFile 
                    ? "bg-green-50 border-green-200 text-green-600" 
                    : "bg-gray-100 border-gray-200 text-gray-600 hover:bg-gray-200"
                }`}
                title="Upload resume - Skills will be auto-extracted"
              >
                {parsingResume ? (
                  <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                )}
                <span className="text-sm font-medium whitespace-nowrap">
                  {parsingResume ? "Reading..." : resumeFile ? "Resume ✓" : "Resume"}
                </span>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={handleResumeUpload}
                  className="hidden"
                  disabled={parsingResume}
                />
              </label>

              {/* Text Input */}
              <div className="flex-1 relative">
                <input
                  type="text"
                  placeholder="Enter target role (e.g., Data Analyst, Software Engineer)..."
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAnalysis()}
                  className="w-full px-4 py-3 bg-gray-100 border border-gray-200 rounded-2xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-white transition-all"
                />
              </div>

              {/* Submit Button */}
              <button
                onClick={handleAnalysis}
                disabled={loading || !targetRole.trim()}
                className="p-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white rounded-xl transition-all disabled:cursor-not-allowed"
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
            <p className="mt-2 text-xs text-center text-gray-400">
              Brutally honest career advice. No sugar-coating.
            </p>
          </div>
        </div>
      </div>

      {/* Timeframe Picker */}
      <TimeframePicker
        isOpen={showTimeframePicker}
        onClose={() => setShowTimeframePicker(false)}
        timeframeValue={timeframeValue}
        timeframeUnit={timeframeUnit}
        onSave={(value, unit) => {
          setTimeframeValue(value);
          setTimeframeUnit(unit);
        }}
      />
    </div>
  );
}
