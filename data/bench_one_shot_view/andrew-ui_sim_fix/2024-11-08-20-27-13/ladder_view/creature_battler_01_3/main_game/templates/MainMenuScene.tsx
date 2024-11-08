import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

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

  if (!props.data?.entities?.player) {
    return (
      <div className="w-full h-full flex items-center justify-center text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="w-full max-w-[177.78vh] aspect-video bg-gradient-to-b from-slate-800 to-slate-900 flex flex-col">
        
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
              variant="default"
              size="lg"
              onClick={() => emitButtonClick('play')}
              className="flex items-center gap-2 px-8 py-6 bg-green-600 hover:bg-green-700 text-xl"
              uid={`play-${props.data.entities.player.uid}`}
            >
              <Play size={24} />
              Play Game
            </Button>
          )}

          {availableButtonSlugs.includes('quit') && (
            <Button
              variant="destructive"
              size="lg"
              onClick={() => emitButtonClick('quit')}
              className="flex items-center gap-2 px-8 py-6 bg-red-600 hover:bg-red-700 text-xl"
              uid={`quit-${props.data.entities.player.uid}`}
            >
              <XCircle size={24} />
              Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
