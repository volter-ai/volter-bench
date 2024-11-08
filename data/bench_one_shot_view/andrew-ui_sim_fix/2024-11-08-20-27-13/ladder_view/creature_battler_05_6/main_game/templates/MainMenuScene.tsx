import { useCurrentButtons } from "@/lib/useChoices";
import { Play, Power } from 'lucide-react'

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: {
        prototype_id: string;
        category: string;
    };
    entities: Record<string, unknown>;
    collections: Record<string, unknown>;
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    };
    stats: Record<string, unknown>;
    meta: Record<string, unknown>;
    collections: Record<string, unknown>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs = [],
        emitButtonClick
    } = useCurrentButtons()

    if (!props.data?.entities?.player) {
        return (
            <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
                <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-b from-blue-900 to-blue-950">
                    <div className="text-white text-xl">Loading...</div>
                </div>
            </div>
        )
    }

    return (
        <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-blue-900 to-blue-950">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        CREATURE BATTLE
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-64">
                    {availableButtonSlugs.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center gap-2 w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                        >
                            <Play size={24} />
                            <span className="text-xl">Play Game</span>
                        </button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center gap-2 w-full px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                        >
                            <Power size={24} />
                            <span className="text-xl">Quit</span>
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
