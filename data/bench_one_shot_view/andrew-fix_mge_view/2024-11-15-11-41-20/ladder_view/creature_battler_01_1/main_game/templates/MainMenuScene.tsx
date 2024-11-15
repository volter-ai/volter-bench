import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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
    <Card className="w-full h-full relative overflow-hidden" style={{ aspectRatio: '16/9' }}>
      <div className="absolute inset-0 bg-gradient-to-b from-slate-800 to-slate-900">
        <div className="h-full flex flex-col items-center justify-between p-8">
          {/* Title Image Section */}
          <div className="flex-1 flex items-center justify-center w-full">
            <div className="w-96 h-32 bg-slate-700 flex items-center justify-center rounded-lg">
              {/* Placeholder for game title image */}
              <span className="text-4xl font-bold text-white opacity-50">
                Game Title Image
              </span>
            </div>
          </div>

          {/* Button Container */}
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
        </div>
      </div>
    </Card>
  );
}
