import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  description: string;
  stats: Record<string, unknown>;
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, unknown>;
  meta: Record<string, unknown>;
  collections: Record<string, unknown>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] aspect-video bg-black bg-opacity-50 flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white text-center">
            {props.data.display_name || "Welcome to the Game"}
          </h1>
        </div>
        <div className="flex gap-4">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig];
            if (!config) return null;
            const Icon = config.icon;
            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="px-6 py-3 bg-white text-purple-600 rounded-lg font-semibold text-lg flex items-center gap-2 hover:bg-purple-100 transition-colors"
              >
                <Icon size={24} />
                {config.text}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
