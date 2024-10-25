import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
    display_name: string,
    description: string,
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
    stats: Record<string, number>,
    meta: Record<string, any>,
    collections: Record<string, any>,
    uid: string,
    display_name: string,
    description: string,
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const buttonConfig = {
        play: { label: "Play", icon: Play },
        quit: { label: "Quit", icon: X },
    };

    return (
        <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9' }}>
            <div className="text-6xl font-bold text-white mt-16">
                {props.data.display_name || "Creature Adventure"}
            </div>

            <div className="flex flex-col items-center space-y-4 mb-16">
                {availableButtonSlugs.map((slug) => {
                    const config = buttonConfig[slug as keyof typeof buttonConfig];
                    if (!config) return null;

                    return (
                        <button
                            key={slug}
                            onClick={() => emitButtonClick(slug)}
                            className="w-48 h-12 text-lg flex items-center justify-center space-x-2 bg-white text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
                        >
                            <config.icon className="w-6 h-6" />
                            <span>{config.label}</span>
                        </button>
                    );
                })}
            </div>

            <div className="text-white text-sm">
                Welcome, {props.data.entities.player?.display_name || "Adventurer"}!
            </div>
        </div>
    );
}
