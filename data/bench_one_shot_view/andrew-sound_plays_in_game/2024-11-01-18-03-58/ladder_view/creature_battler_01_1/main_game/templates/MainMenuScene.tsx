import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  }

  const playerName = data?.entities?.player?.display_name || 'Adventurer'

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9' }}>
      <div className="text-6xl font-bold text-white mt-16">
        Creature Adventure
      </div>

      <div className="text-2xl text-white">
        Welcome, {playerName}!
      </div>

      <div className="flex flex-col space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig]
          if (!config) return null

          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-white text-purple-600 px-8 py-3 rounded-full font-semibold text-xl flex items-center justify-center space-x-2 hover:bg-purple-100 transition-colors"
            >
              <config.icon className="w-6 h-6" />
              <span>{config.text}</span>
            </button>
          )
        })}
      </div>

      {!availableButtonSlugs.length && (
        <div className="text-white text-xl">
          Loading game options...
        </div>
      )}
    </div>
  )
}
