"use client";

import { useState, useEffect } from "react";
import {
  BookOpen,
  Wrench,
  Monitor,
  Video,
  Truck,
  Zap,
  Briefcase,
  Calendar,
  Github,
  ExternalLink,
  Play,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

interface Task {
  id: string;
  label: string;
  url?: string;
}

interface Section {
  id: string;
  title: string;
  icon: React.ReactNode;
  subsections?: {
    title: string;
    tasks: Task[];
    notesKey: string;
  }[];
  tasks?: Task[];
  notesKey?: string;
  checklist?: string[];
  schedule?: { week: string; focus: string }[];
}

const sections: Section[] = [
  {
    id: "foundations",
    title: "1. Foundations: Understanding AI & Video Workflow",
    icon: <BookOpen className="w-6 h-6" />,
    tasks: [
      {
        id: "f1",
        label: "Watch What are Large Language Models?",
        url: "https://www.youtube.com/watch?v=vw6E7gK4Dtk",
      },
      {
        id: "f2",
        label: "Watch AI Models Explained Simply",
        url: "https://www.youtube.com/watch?v=xx310zM3tLs",
      },
      {
        id: "f3",
        label: "Watch Tokens Explained",
        url: "https://www.youtube.com/watch?v=zizonToFXDs",
      },
      {
        id: "f4",
        label: "Watch How AI text to image to voice to video works",
        url: "https://www.youtube.com/watch?v=KbcZ2WckxEs",
      },
      {
        id: "f5",
        label: "Watch AI video content explained (short)",
        url: "https://www.youtube.com/watch?v=MsGg4WXPynk",
      },
    ],
    notesKey: "notes_foundations",
  },
  {
    id: "core-tools",
    title: "2. Core Tools Training",
    icon: <Wrench className="w-6 h-6" />,
    subsections: [
      {
        title: "A. Scriptwriting (LLM)",
        tasks: [
          {
            id: "ct_a1",
            label: "Watch How to use Anthropic Claude",
            url: "https://www.youtube.com/watch?v=ZS8KJqLa5PE",
          },
          {
            id: "ct_a2",
            label: "Watch Prompting Basics (Beginner-Friendly)",
            url: "https://www.youtube.com/watch?v=-1h5Nw2Z2jE",
          },
          { id: "ct_a3", label: "Practice: write a 15s script" },
          { id: "ct_a4", label: "Practice: write a 30s script" },
          { id: "ct_a5", label: "Practice: rewrite script in Dutch" },
          {
            id: "ct_a6",
            label: "Practice: adjust tone (e.g. energetic, warm, corporate)",
          },
        ],
        notesKey: "notes_scriptwriting",
      },
      {
        title: "B. Image Generation (Replicate / fal.ai)",
        tasks: [
          {
            id: "ct_b1",
            label: "Watch What is diffusion / image generation?",
            url: "https://www.youtube.com/watch?v=0pDE4VX_9Kk",
          },
          {
            id: "ct_b2",
            label: "Watch Replicate Tutorial: How to run models",
            url: "https://www.youtube.com/watch?v=mcSCTWJFe8E",
          },
          { id: "ct_b3", label: "Practice: generate 5 images using Flux Schnell" },
          {
            id: "ct_b4",
            label: "Practice: adjust style (cinematic, soft, bold colors)",
          },
          {
            id: "ct_b5",
            label:
              "Practice: generate images for Dutch bakery scene (or any test scene)",
          },
        ],
        notesKey: "notes_image_gen",
      },
      {
        title: "C. Voice Generation (ElevenLabs)",
        tasks: [
          {
            id: "ct_c1",
            label: "Watch ElevenLabs Beginner Tutorial",
            url: "https://www.youtube.com/watch?v=rxF3zGF7s84",
          },
          {
            id: "ct_c2",
            label: "Watch How voice cloning & TTS works",
            url: "https://www.youtube.com/watch?v=E0uS1MQoQv0",
          },
          { id: "ct_c3", label: "Practice: use Dutch male voice (Adam)" },
          { id: "ct_c4", label: "Practice: use Dutch female voice (Rachel)" },
          { id: "ct_c5", label: "Experiment: adjust speed, pitch, style" },
        ],
        notesKey: "notes_voice_gen",
      },
    ],
  },
  {
    id: "github-basics",
    title: "3. GitHub Basics: Understanding Your Backend",
    icon: <Github className="w-6 h-6" />,
    tasks: [
      {
        id: "gh1",
        label: "Watch What is Git & GitHub? (Beginner)",
        url: "https://www.youtube.com/watch?v=8Dd7KRpKeaE",
      },
      {
        id: "gh2",
        label: "Watch Git Explained in 100 Seconds",
        url: "https://www.youtube.com/watch?v=hwP7WQkmECE",
      },
      {
        id: "gh3",
        label: "Watch How to Navigate GitHub Repositories",
        url: "https://www.youtube.com/watch?v=iv8rSLsi1xo",
      },
      {
        id: "gh4",
        label: "Watch Understanding Branches & Commits",
        url: "https://www.youtube.com/watch?v=oPpnCh7InLY",
      },
      {
        id: "gh5",
        label: "Watch GitHub Pull Requests Explained",
        url: "https://www.youtube.com/watch?v=For9VtrQx58",
      },
      {
        id: "gh6",
        label: "Practice: Navigate to the BOM Studios repository",
      },
      {
        id: "gh7",
        label: "Practice: Find and read the README file",
      },
      {
        id: "gh8",
        label: "Practice: Browse the code structure (engine/, api/, portal/)",
      },
      {
        id: "gh9",
        label: "Practice: View recent commits and understand what changed",
      },
      {
        id: "gh10",
        label: "Practice: Find the .env.example file to understand configuration",
      },
    ],
    notesKey: "notes_github",
  },
  {
    id: "local-setup",
    title: "4. Local Setup & Running BOM Studios",
    icon: <Monitor className="w-6 h-6" />,
    tasks: [
      {
        id: "ls1",
        label: "Watch FFmpeg Crash Course (Beginner)",
        url: "https://www.youtube.com/watch?v=26d9SxE7iPo",
      },
      {
        id: "ls2",
        label: "Watch Ken Burns effect explanation",
        url: "https://www.youtube.com/watch?v=rdwz7QiVQK0",
      },
      {
        id: "ls3",
        label: "Watch What is an API (Beginner Explanation)",
        url: "https://www.youtube.com/watch?v=GZvSYJDk-us",
      },
      {
        id: "ls4",
        label: "Watch How backends and frontends talk",
        url: "https://www.youtube.com/watch?v=7YcW25PHnAA",
      },
      {
        id: "ls5",
        label: "Watch How to install Python",
        url: "https://www.youtube.com/watch?v=Kn1HF3oD19c",
      },
      {
        id: "ls6",
        label: "Watch How to run FastAPI locally (beginner tutorial)",
        url: "https://www.youtube.com/watch?v=0RS-M7t_TTg",
      },
      {
        id: "ls7",
        label: "Install dependencies, configure .env, ensure API keys present",
      },
      { id: "ls8", label: "Run the backend locally (uvicorn ...)" },
      { id: "ls9", label: "Test health endpoint: http://localhost:8000/health" },
    ],
    notesKey: "notes_local_setup",
    checklist: [
      "FFmpeg installed and functioning",
      'API returns "OK" on health endpoint',
      "Environment variables properly set",
    ],
  },
  {
    id: "first-video",
    title: "5. First Real Video - Full Pipeline",
    icon: <Video className="w-6 h-6" />,
    tasks: [
      {
        id: "fv1",
        label: "Watch End-to-end AI video workflow overview",
        url: "https://www.youtube.com/watch?v=6gG8LqyEZZ8",
      },
      {
        id: "fv2",
        label: "Trigger the test endpoint (e.g. via curl or Postman)",
      },
      {
        id: "fv3",
        label:
          "Monitor logs while script, images, voice, and video are generated",
      },
      { id: "fv4", label: "Retrieve the output MP4" },
      { id: "fv5", label: "Review the video" },
    ],
    notesKey: "notes_first_video",
    checklist: [
      "No error messages",
      "Images look coherent, follow script scenes",
      "Voice matches script and language",
      "Final video resolution / aspect ratio fine",
      "Video length as expected",
    ],
  },
  {
    id: "operations",
    title: "6. Operational Skills: Delivering & Reviewing Videos",
    icon: <Truck className="w-6 h-6" />,
    tasks: [
      {
        id: "op1",
        label: "Watch Google Drive Sharing Basics",
        url: "https://www.youtube.com/watch?v=Tpe7RMm7R0U",
      },
      { id: "op2", label: "Upload a generated video to Drive, share link" },
      {
        id: "op3",
        label: "Watch How to evaluate short-form videos",
        url: "https://www.youtube.com/watch?v=zKJc2pQmT9A",
      },
      {
        id: "op4",
        label: "Review the video critically: hook, visuals, voice, CTA, cohesion",
      },
      {
        id: "op5",
        label: "(Optional) Watch CapCut Beginner Tutorial for small edits",
        url: "https://www.youtube.com/watch?v=sRlE6O1Sm6A",
      },
    ],
    notesKey: "notes_operations",
  },
  {
    id: "automation",
    title: "7. Automation & Scaling (Phase 2)",
    icon: <Zap className="w-6 h-6" />,
    tasks: [
      {
        id: "au1",
        label: "Watch Tally Forms Beginner Guide",
        url: "https://www.youtube.com/watch?v=aDAFzR2yVQI",
      },
      {
        id: "au2",
        label: "Build a simple client intake form (with sample fields)",
      },
      {
        id: "au3",
        label: "Watch n8n for Beginners",
        url: "https://www.youtube.com/watch?v=jOqJ0NVsB7Q",
      },
      {
        id: "au4",
        label:
          "Sketch a workflow: form to backend to video generation to email/drive share",
      },
      {
        id: "au5",
        label: "(Optional) Watch How Vercel Works (for beginners)",
        url: "https://www.youtube.com/watch?v=ZV6v2ZlMTaE",
      },
      {
        id: "au6",
        label: "(Optional) Watch DigitalOcean App Platform Tutorial",
        url: "https://www.youtube.com/watch?v=2QA2Jm2X0iM",
      },
    ],
    notesKey: "notes_automation",
  },
  {
    id: "business-skills",
    title: "8. Business & Client Management Skills",
    icon: <Briefcase className="w-6 h-6" />,
    tasks: [
      {
        id: "bs1",
        label: "Watch How to explain AI video simply",
        url: "https://www.youtube.com/watch?v=8s0CM-y48lI",
      },
      {
        id: "bs2",
        label: "Watch How short-form video drives sales",
        url: "https://www.youtube.com/watch?v=XzGZt2v5BRU",
      },
      {
        id: "bs3",
        label: 'Practice: Draft a "How it works" explanation for clients',
      },
      { id: "bs4", label: "Practice: Define simple pricing & ROI explanation" },
      {
        id: "bs5",
        label: 'Write a short "Service Offering Summary" (1-paragraph pitch)',
      },
    ],
    notesKey: "notes_business",
  },
  {
    id: "schedule",
    title: "9. Suggested 4-Week Schedule",
    icon: <Calendar className="w-6 h-6" />,
    schedule: [
      {
        week: "Week 1",
        focus: "Foundations + Core Tools (Script / Image / Voice) + GitHub Basics",
      },
      { week: "Week 2", focus: "Local Setup + First Video + Review" },
      {
        week: "Week 3",
        focus: "Delivery Workflow + Quality Review + Basic Editing",
      },
      {
        week: "Week 4",
        focus: "Automation Setup + Form & Workflow Design + Basic Business Pitch",
      },
    ],
  },
];

const tableOfContents = [
  { id: "foundations", label: "Foundations: Understanding AI & Video Workflow" },
  { id: "core-tools", label: "Core Tools Training" },
  { id: "github-basics", label: "GitHub Basics: Understanding Your Backend" },
  { id: "local-setup", label: "Local Setup & Running BOM Studios" },
  { id: "first-video", label: "First Real Video - Full Pipeline" },
  { id: "operations", label: "Operational Skills: Delivering & Reviewing Videos" },
  { id: "automation", label: "Automation & Scaling (Phase 2)" },
  { id: "business-skills", label: "Business & Client Management Skills" },
  { id: "schedule", label: "Suggested 4-Week Schedule" },
];

export default function CoursePage() {
  const [completed, setCompleted] = useState<Record<string, boolean>>({});
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const savedCompleted = localStorage.getItem("bom_course_completed");
    const savedNotes = localStorage.getItem("bom_course_notes");
    const savedExpanded = localStorage.getItem("bom_course_expanded");

    if (savedCompleted) setCompleted(JSON.parse(savedCompleted));
    if (savedNotes) setNotes(JSON.parse(savedNotes));
    if (savedExpanded) {
      setExpandedSections(JSON.parse(savedExpanded));
    } else {
      // Default: all sections expanded
      const defaultExpanded: Record<string, boolean> = {};
      sections.forEach((s) => (defaultExpanded[s.id] = true));
      setExpandedSections(defaultExpanded);
    }
    setIsLoaded(true);
  }, []);

  // Save to localStorage on changes
  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem("bom_course_completed", JSON.stringify(completed));
    }
  }, [completed, isLoaded]);

  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem("bom_course_notes", JSON.stringify(notes));
    }
  }, [notes, isLoaded]);

  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem("bom_course_expanded", JSON.stringify(expandedSections));
    }
  }, [expandedSections, isLoaded]);

  const toggleTask = (taskId: string) => {
    setCompleted((prev) => ({ ...prev, [taskId]: !prev[taskId] }));
  };

  const updateNotes = (key: string, value: string) => {
    setNotes((prev) => ({ ...prev, [key]: value }));
  };

  const toggleSection = (sectionId: string) => {
    setExpandedSections((prev) => ({ ...prev, [sectionId]: !prev[sectionId] }));
  };

  // Calculate progress
  const allTasks: string[] = [];
  sections.forEach((section) => {
    if (section.tasks) {
      section.tasks.forEach((t) => allTasks.push(t.id));
    }
    if (section.subsections) {
      section.subsections.forEach((sub) => {
        sub.tasks.forEach((t) => allTasks.push(t.id));
      });
    }
  });

  const completedCount = allTasks.filter((id) => completed[id]).length;
  const progressPercent = allTasks.length > 0 ? (completedCount / allTasks.length) * 100 : 0;

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-steel-grey">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-warm-white">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-bom-black text-warm-white py-4 px-6 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="font-heading text-xl">BOM Studios</h1>
            <p className="text-silver-mist text-sm">Jeroen Course Page</p>
          </div>
          <div className="text-right">
            <div className="text-sm text-silver-mist mb-1">
              Progress: {completedCount} / {allTasks.length} tasks
            </div>
            <div className="w-48 progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="section-card mb-8">
          <h2 className="font-heading text-2xl text-bom-black mb-4">
            Welcome to Your Course
          </h2>
          <p className="text-slate-grey mb-4">
            This is your step-by-step course to learn everything needed to operate
            BOM Studios from zero to a fully functional video-generation business.
            Work through section by section. As you complete each task, check the
            boxes to track your progress.
          </p>
          <div className="bg-silver-mist/50 rounded-lg p-4">
            <h3 className="font-semibold text-slate-grey mb-2">How to use:</h3>
            <ul className="text-steel-grey text-sm space-y-1">
              <li>
                Work top-to-bottom. You can skip ahead, but recommended order is
                from Foundation to Core Tools to Local Setup to First Video to
                Operations to Automation to Business Skills.
              </li>
              <li>
                Use the checkboxes to mark tasks done - your progress is saved
                automatically.
              </li>
              <li>Below each section there&apos;s space for your own notes.</li>
            </ul>
          </div>
        </div>

        {/* Table of Contents */}
        <div className="section-card mb-8">
          <h2 className="font-heading text-xl text-bom-black mb-4">
            Table of Contents
          </h2>
          <nav>
            <ol className="space-y-2">
              {tableOfContents.map((item, index) => (
                <li key={item.id}>
                  <a
                    href={`#${item.id}`}
                    className="text-stone-blue hover:text-bom-black transition-colors flex items-center gap-2"
                  >
                    <span className="text-steel-grey">{index + 1}.</span>
                    {item.label}
                  </a>
                </li>
              ))}
            </ol>
          </nav>
        </div>

        {/* Course Sections */}
        {sections.map((section) => (
          <section key={section.id} id={section.id} className="section-card">
            {/* Section Header */}
            <button
              onClick={() => toggleSection(section.id)}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center gap-3">
                <div className="text-stone-blue">{section.icon}</div>
                <h2 className="font-heading text-lg text-bom-black">
                  {section.title}
                </h2>
              </div>
              {expandedSections[section.id] ? (
                <ChevronUp className="w-5 h-5 text-steel-grey" />
              ) : (
                <ChevronDown className="w-5 h-5 text-steel-grey" />
              )}
            </button>

            {expandedSections[section.id] && (
              <div className="mt-6">
                {/* Regular tasks */}
                {section.tasks && (
                  <div className="space-y-3">
                    {section.tasks.map((task) => (
                      <TaskItem
                        key={task.id}
                        task={task}
                        completed={completed[task.id]}
                        onToggle={() => toggleTask(task.id)}
                      />
                    ))}
                  </div>
                )}

                {/* Subsections */}
                {section.subsections &&
                  section.subsections.map((sub, idx) => (
                    <div key={idx} className={idx > 0 ? "mt-8" : ""}>
                      <h3 className="font-semibold text-slate-grey mb-4">
                        {sub.title}
                      </h3>
                      <div className="space-y-3">
                        {sub.tasks.map((task) => (
                          <TaskItem
                            key={task.id}
                            task={task}
                            completed={completed[task.id]}
                            onToggle={() => toggleTask(task.id)}
                          />
                        ))}
                      </div>
                      {/* Subsection notes */}
                      <div className="mt-4">
                        <label className="block text-sm text-steel-grey mb-2">
                          Notes / Lessons Learned:
                        </label>
                        <textarea
                          className="notes-textarea"
                          placeholder="Write down examples and what worked / what didn't..."
                          value={notes[sub.notesKey] || ""}
                          onChange={(e) =>
                            updateNotes(sub.notesKey, e.target.value)
                          }
                        />
                      </div>
                    </div>
                  ))}

                {/* Checklist */}
                {section.checklist && (
                  <div className="mt-6 bg-sage/10 rounded-lg p-4">
                    <h4 className="font-semibold text-slate-grey mb-3">
                      What to Verify:
                    </h4>
                    <ul className="space-y-2">
                      {section.checklist.map((item, idx) => (
                        <li
                          key={idx}
                          className="flex items-center gap-2 text-steel-grey"
                        >
                          <span className="text-sage">&#10003;</span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Schedule table */}
                {section.schedule && (
                  <div className="mt-4">
                    <table className="w-full border-collapse">
                      <thead>
                        <tr className="border-b-2 border-silver-mist">
                          <th className="text-left py-2 px-3 text-slate-grey font-semibold">
                            Week
                          </th>
                          <th className="text-left py-2 px-3 text-slate-grey font-semibold">
                            Focus
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {section.schedule.map((row, idx) => (
                          <tr
                            key={idx}
                            className="border-b border-silver-mist/50"
                          >
                            <td className="py-3 px-3 text-stone-blue font-medium">
                              {row.week}
                            </td>
                            <td className="py-3 px-3 text-steel-grey">
                              {row.focus}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    <p className="text-sm text-steel-grey mt-4 italic">
                      You can flex the timeline depending on your pace. The key is
                      consistent progress.
                    </p>
                  </div>
                )}

                {/* Section notes (if not subsections) */}
                {section.notesKey && !section.subsections && (
                  <div className="mt-6">
                    <label className="block text-sm text-steel-grey mb-2">
                      Notes / What to Learn:
                    </label>
                    <textarea
                      className="notes-textarea"
                      placeholder="Use this space to write down key insights..."
                      value={notes[section.notesKey] || ""}
                      onChange={(e) =>
                        updateNotes(section.notesKey!, e.target.value)
                      }
                    />
                  </div>
                )}
              </div>
            )}
          </section>
        ))}

        {/* Final Notes */}
        <div className="section-card mt-8 bg-stone-blue/10">
          <h2 className="font-heading text-xl text-bom-black mb-4">
            Final Notes
          </h2>
          <p className="text-slate-grey">
            By working through this course, you&apos;ll build confidence running BOM
            Studios from scratch, know how each component works under the hood,
            and be ready to deliver quality videos - and even start automating
            the process for clients.
          </p>
          <p className="text-slate-grey mt-4">
            Whenever you finish a section, come back here, check it off, and
            reflect on what you learned.
          </p>
        </div>

        {/* Reset Progress */}
        <div className="mt-8 text-center">
          <button
            onClick={() => {
              if (
                confirm(
                  "Are you sure you want to reset all progress? This cannot be undone."
                )
              ) {
                setCompleted({});
                setNotes({});
                localStorage.removeItem("bom_course_completed");
                localStorage.removeItem("bom_course_notes");
              }
            }}
            className="text-sm text-steel-grey hover:text-bom-black transition-colors underline"
          >
            Reset all progress
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-bom-black text-silver-mist py-6 mt-12">
        <div className="max-w-4xl mx-auto px-6 text-center text-sm">
          <p>BOM Studios &copy; {new Date().getFullYear()}</p>
        </div>
      </footer>
    </div>
  );
}

function TaskItem({
  task,
  completed,
  onToggle,
}: {
  task: Task;
  completed: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="flex items-start gap-3">
      <input
        type="checkbox"
        className="task-checkbox mt-0.5"
        checked={completed || false}
        onChange={onToggle}
      />
      <label
        className={`flex-1 cursor-pointer ${
          completed ? "task-label completed" : "text-slate-grey"
        }`}
        onClick={onToggle}
      >
        {task.url ? (
          <span className="flex items-center gap-2 flex-wrap">
            <span>{task.label}</span>
            <a
              href={task.url}
              target="_blank"
              rel="noopener noreferrer"
              className="video-link text-sm"
              onClick={(e) => e.stopPropagation()}
            >
              <Play className="w-4 h-4" />
              <span>Watch</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </span>
        ) : (
          task.label
        )}
      </label>
    </div>
  );
}
