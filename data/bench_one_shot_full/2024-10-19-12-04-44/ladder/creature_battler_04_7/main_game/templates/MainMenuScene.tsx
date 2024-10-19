import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-center shadow-lg">
          {props.data.display_name || "Game Title"}
        </h1>
      </div>

      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;

          return (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="w-48 text-lg flex items-center justify-center space-x-2"
            >
              <config.icon className="w-5 h-5" />
              <span>{config.text}</span>
            </Button>
          );
        })}
      </div>
    </div>
  );
}
