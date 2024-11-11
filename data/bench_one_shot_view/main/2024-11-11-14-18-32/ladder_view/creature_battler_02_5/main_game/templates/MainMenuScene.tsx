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
    creatures: BaseEntity[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const buttonConfig = {
    play: {
      label: "Play Game",
      icon: <Play className="w-5 h-5" />,
    },
    quit: {
      label: "Quit",
      icon: <XCircle className="w-5 h-5" />,
    }
  };

  return (
    <Card className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8 border-0">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white tracking-wider">
          {props.data.display_name}
        </h1>
      </div>

      <div className="flex flex-col gap-4 mb-12 w-64">
        {Object.entries(buttonConfig).map(([slug, config]) => (
          availableButtonSlugs.includes(slug) && (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="w-full flex items-center justify-center gap-2"
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
  );
}
