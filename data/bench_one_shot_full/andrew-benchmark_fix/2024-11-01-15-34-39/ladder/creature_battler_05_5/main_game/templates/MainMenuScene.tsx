import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col items-center justify-between p-8">
      <div className="flex-grow flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white text-center">
          Creature Battle Game
        </h1>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {Object.entries(buttonConfig).map(([slug, { text, icon: Icon }]) => (
          availableButtonSlugs.includes(slug) && (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-white text-purple-600 font-bold py-2 px-4 rounded-full flex items-center space-x-2 hover:bg-purple-100 transition-colors"
            >
              <Icon size={24} />
              <span>{text}</span>
            </button>
          )
        ))}
      </div>

      <div className="mt-4 text-white text-center">
        <p>Welcome, {props.data.entities.player?.display_name || "Player"}!</p>
      </div>
    </div>
  );
}
