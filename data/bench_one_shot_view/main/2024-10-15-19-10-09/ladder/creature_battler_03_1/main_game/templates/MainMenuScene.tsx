import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
      meta: Record<string, any>;
      entities: Record<string, any>;
      collections: Record<string, any>;
      display_name: string;
      description: string;
    };
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 p-8">
      <div className="w-full h-1/3 flex items-center justify-center">
        <div className="bg-white bg-opacity-20 rounded-lg p-8 text-4xl font-bold text-white">
          Game Title
        </div>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {Object.entries(buttonConfig).map(([slug, config]) => {
          if (availableButtonSlugs.includes(slug)) {
            return (
              <Button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="w-48 h-12 text-lg flex items-center justify-center space-x-2"
              >
                <config.icon className="w-6 h-6" />
                <span>{config.text}</span>
              </Button>
            );
          }
          return null;
        })}
      </div>

      <div className="text-white text-sm mt-4">
        {props.data.entities.player?.display_name || "Unknown Player"}
      </div>
    </div>
  );
}
