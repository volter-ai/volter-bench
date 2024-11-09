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
    creatures: BaseEntity[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const buttonConfig = {
    play: {
      label: "Play Game",
      icon: <Play className="w-6 h-6" />,
    },
    quit: {
      label: "Quit",
      icon: <XCircle className="w-6 h-6" />,
    }
  };

  if (!props.data) {
    return null;
  }

  return (
    <Card className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8 rounded-none border-0">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white tracking-wider">
          {props.data.display_name ?? "Main Menu"}
        </h1>
      </div>

      <Card className="bg-slate-800/50 p-6 rounded-lg border-slate-700">
        <div className="flex flex-col gap-4">
          {Object.entries(buttonConfig).map(([slug, config]) => (
            availableButtonSlugs.includes(slug) && (
              <Button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="flex items-center justify-center gap-2 px-8 py-6 text-lg"
                variant="secondary"
                size="lg"
              >
                {config.icon}
                {config.label}
              </Button>
            )
          ))}
        </div>
      </Card>
    </Card>
  );
}
