// Do not change these imports:
import {useCurrentButtons} from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react'
import { Button } from "@/components/ui/button"

interface Stats {
    [key: string]: number
}

interface Meta {
    prototype_id: string
    category: string
    [key: string]: any
}

interface Skill {
    uid: string
    stats: Stats
    meta: Meta
    entities: Record<string, any>
    collections: Record<string, any>
    display_name: string
    description: string
}

interface Creature {
    uid: string
    stats: Stats
    meta: Meta
    entities: Record<string, any>
    collections: {
        skills: Skill[]
    }
    display_name: string
    description: string
}

interface Player {
    uid: string
    stats: Stats
    meta: Meta
    entities: Record<string, any>
    collections: {
        creatures: Creature[]
    }
    display_name: string
    description: string
}

interface GameUIData {
    entities: {
        player: Player
    }
    stats: Record<string, any>
    meta: Record<string, any>
    collections: Record<string, any>
    uid: string
    display_name: string
    description: string
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props?.data?.display_name ?? 'CREATURE BATTLE'}
                </h1>
            </div>

            <div className="flex-1" />

            <div className="flex-1 flex flex-col items-center justify-center gap-4">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-2 px-8 py-6 text-xl"
                        variant="default"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-2 px-8 py-6 text-xl"
                        variant="destructive"
                    >
                        <XCircle className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
