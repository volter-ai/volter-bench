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

interface BaseEntity {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  collections: {
    creatures: Creature[];
  };
}

interface Creature extends BaseEntity {
  stats: GameStats & {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Skill extends BaseEntity {
  stats: GameStats & {
    damage: number;
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="w-full max-w-[177.78vh] aspect-video bg-gradient-to-b from-slate-800 to-slate-900 flex flex-col">
        <Card className="m-8 flex-1 flex flex-col bg-black/40 backdrop-blur">
          {/* Title Section */}
          <div className="flex-1 flex items-center justify-center">
            <h1 className="text-6xl font-bold text-white tracking-wider">
              GAME TITLE
            </h1>
          </div>

          {/* Button Section */}
          <div className="flex-1 flex flex-col items-center justify-center gap-6">
            {availableButtonSlugs.includes('play') && (
              <Button
                uid="play_button"
                variant="default"
                size="lg"
                onClick={() => emitButtonClick('play')}
                className="flex items-center gap-2 px-8 py-6 text-xl"
              >
                <Play className="w-6 h-6" />
                Play Game
              </Button>
            )}

            {availableButtonSlugs.includes('quit') && (
              <Button
                uid="quit_button"
                variant="destructive"
                size="lg"
                onClick={() => emitButtonClick('quit')}
                className="flex items-center gap-2 px-8 py-6 text-xl"
              >
                <XCircle className="w-6 h-6" />
                Quit
              </Button>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
