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

interface Skill {
  __type: string;
  stats: {
    base_damage: number;
  };
  meta: GameMeta;
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
    attack: number;
    defense: number;
    speed: number;
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
  __type: string;
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

interface MainMenuScene {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: {
    player: Player;
  };
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
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

  if (!props.data) {
    return (
      <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex items-center justify-center">
        <p className="text-white text-xl">Loading...</p>
      </div>
    );
  }

  return (
    <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8 overflow-hidden">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white tracking-wider text-center">
          {props.data?.entities?.player?.display_name || "Creature Game"}
        </h1>
      </div>

      <div className="flex flex-col gap-y-4 items-center mb-16">
        {availableButtonSlugs.includes('play') && (
          <Button
            variant="default"
            size="lg"
            onClick={() => emitButtonClick('play')}
            className="flex items-center gap-x-2 bg-green-600 hover:bg-green-700 text-xl px-8 py-6"
          >
            <Play className="w-6 h-6" />
            Play Game
          </Button>
        )}

        {availableButtonSlugs.includes('quit') && (
          <Button
            variant="destructive"
            size="lg"
            onClick={() => emitButtonClick('quit')}
            className="flex items-center gap-x-2 text-xl px-8 py-6"
          >
            <XCircle className="w-6 h-6" />
            Quit
          </Button>
        )}
      </div>
    </div>
  );
}
