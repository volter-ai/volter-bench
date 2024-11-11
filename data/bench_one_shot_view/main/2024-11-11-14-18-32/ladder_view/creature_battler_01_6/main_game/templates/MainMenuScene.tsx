// Do not change these imports:
import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Card} from "@/components/ui/card";

import { Play, XCircle } from 'lucide-react'

interface Skill {
  __type: string;
  stats: {
    damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
  entities: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
  entities: Record<string, any>;
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: string;
  stats: Record<string, any>;
  meta: {
    prototype_id: string;
    category: string;
  };
  entities: Record<string, any>;
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  __type: string;
  stats: Record<string, any>;
  meta: Record<string, any>;
  entities: {
    player: Player;
  };
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  return (
    <div className="relative w-full h-0 pb-[56.25%]"> {/* 16:9 aspect ratio container */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-800 to-slate-900 flex flex-col items-center justify-between p-8">
        <Card className="w-full max-w-4xl mt-12 flex items-center justify-center bg-transparent border-none">
          <h1 className="text-6xl font-bold text-white tracking-wider">
            {props.data?.display_name || "Game Title"}
          </h1>
        </Card>

        <Card className="w-full max-w-md mb-12 bg-transparent border-none">
          <div className="flex flex-col gap-4">
            {availableButtonSlugs.includes('play') && (
              <button
                onClick={() => emitButtonClick('play')}
                className="flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white py-4 px-8 rounded-lg text-xl transition-colors"
              >
                <Play className="w-6 h-6" />
                Play Game
              </button>
            )}

            {availableButtonSlugs.includes('quit') && (
              <button
                onClick={() => emitButtonClick('quit')}
                className="flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white py-4 px-8 rounded-lg text-xl transition-colors"
              >
                <XCircle className="w-6 h-6" />
                Quit
              </button>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
