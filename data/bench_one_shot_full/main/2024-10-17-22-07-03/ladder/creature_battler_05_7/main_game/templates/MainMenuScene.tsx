import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface GameUIData {
    entities: {
        player: {
            uid: string;
            display_name: string;
        }
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const gameTitle = "Creature Battle"

    const buttonConfig = {
        play: { text: "Play", icon: Play },
        quit: { text: "Quit", icon: X },
    }

    return (
        <div className="h-screen w-screen flex items-center justify-center bg-gradient-to-b from-blue-900 to-blue-700">
            <div className="w-full max-w-[177.78vh] aspect-video flex flex-col justify-between items-center p-8">
                <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
                    {gameTitle}
                </h1>
                <div className="flex flex-col space-y-4 mb-16">
                    {availableButtonSlugs.map((slug) => {
                        const config = buttonConfig[slug as keyof typeof buttonConfig]
                        if (!config) return null
                        const Icon = config.icon
                        return (
                            <button
                                key={slug}
                                onClick={() => emitButtonClick(slug)}
                                className="flex items-center justify-center space-x-2 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-lg transition-colors duration-200"
                            >
                                <Icon size={24} />
                                <span>{config.text}</span>
                            </button>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}
