import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
}

interface Skill {
  __type: "Skill";
  stats: {
    damage: number;
  };
  meta: GameMeta;
  entities: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: GameMeta;
  entities: Record<string, any>;
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  return (
    <div className="relative w-full h-full">
      {/* 16:9 Container */}
      <div className="absolute inset-0 w-full h-full">
        <div className="relative w-full h-0 pb-[56.25%]">
          <Card className="absolute inset-0 bg-gradient-to-b from-slate-800 to-slate-900 flex flex-col items-center justify-between p-8 overflow-hidden">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center w-full">
              <div className="relative w-full max-w-2xl h-32">
                {/* Placeholder for game title image - would be replaced with actual image component */}
                <div className="w-full h-full bg-slate-700 rounded-lg flex items-center justify-center">
                  <h1 className="text-4xl font-bold text-white tracking-wider">
                    {props.data?.display_name || "Game Title"}
                  </h1>
                </div>
              </div>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 w-full max-w-md">
              {availableButtonSlugs.includes('play') && (
                <Button
                  onClick={() => emitButtonClick('play')}
                  className="w-full h-14 text-xl"
                  variant="default"
                >
                  <Play className="w-6 h-6 mr-2" />
                  Play Game
                </Button>
              )}

              {availableButtonSlugs.includes('quit') && (
                <Button
                  onClick={() => emitButtonClick('quit')}
                  className="w-full h-14 text-xl"
                  variant="destructive"
                >
                  <XCircle className="w-6 h-6 mr-2" />
                  Quit
                </Button>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
