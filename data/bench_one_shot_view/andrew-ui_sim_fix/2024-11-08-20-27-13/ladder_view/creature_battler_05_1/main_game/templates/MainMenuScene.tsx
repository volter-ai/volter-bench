import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, Power } from 'lucide-react'
import { Button } from "@/components/ui/button"

interface Stats {
    [key: string]: number
}

interface Meta {
    prototype_id: string
    category: string
    [key: string]: string
}

interface BaseEntity {
    __type: string
    uid: string
    display_name: string
    description: string
    stats: Stats
    meta: Meta
    entities: Record<string, BaseEntity>
    collections: Record<string, BaseEntity[]>
}

interface Player extends BaseEntity {
    __type: 'Player'
}

interface GameUIData {
    entities: {
        player: Player
    }
    stats: Stats
    meta: Meta
    collections: Record<string, BaseEntity[]>
    uid: string
    display_name: string
    description: string
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    // Safely handle missing data
    if (!props.data) {
        return null
    }

    return (
        <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-slate-900 to-slate-800 aspect-video p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    CREATURE BATTLE
                </h1>
            </div>

            <div className="flex flex-col gap-4 w-64">
                {availableButtonSlugs.includes('play') && (
                    <Button 
                        variant="default"
                        size="lg"
                        onClick={() => emitButtonClick('play')}
                        className="w-full bg-emerald-600 hover:bg-emerald-500"
                    >
                        <Play className="mr-2 h-5 w-5" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        variant="destructive"
                        size="lg"
                        onClick={() => emitButtonClick('quit')}
                        className="w-full"
                    >
                        <Power className="mr-2 h-5 w-5" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
