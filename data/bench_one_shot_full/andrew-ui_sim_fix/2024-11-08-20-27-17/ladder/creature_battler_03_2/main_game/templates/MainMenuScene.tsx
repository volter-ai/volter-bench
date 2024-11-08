import {useCurrentButtons} from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button"

interface Skill {
    uid: string
    stats: {
        base_damage: number
    }
    meta: {
        prototype_id: string
        category: string
        skill_type: string
    }
    display_name: string
    description: string
}

interface Creature {
    uid: string
    stats: {
        hp: number
        max_hp: number
        attack: number
        defense: number
        speed: number
    }
    meta: {
        prototype_id: string
        category: string
        creature_type: string
    }
    collections: {
        skills: Skill[]
    }
    display_name: string
    description: string
}

interface Player {
    uid: string
    stats: Record<string, number>
    meta: {
        prototype_id: string
        category: string
    }
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
    meta: Record<string, unknown>
    collections: Record<string, unknown>
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
        <div className="w-full h-screen bg-gradient-to-b from-slate-900 to-slate-800 flex items-center justify-center">
            <div className="relative w-full max-w-[177.78vh] h-full max-h-[56.25vw]">
                <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                    {/* Title Section */}
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            {props.data?.display_name || "GAME TITLE"}
                        </h1>
                    </div>

                    {/* Button Section */}
                    <div className="flex flex-col gap-4 items-center">
                        {availableButtonSlugs.includes('play') && (
                            <Button
                                onClick={() => emitButtonClick('play')}
                                className="flex items-center gap-2 px-8 py-6 text-xl"
                                size="lg"
                            >
                                <Play className="w-6 h-6" />
                                Play Game
                            </Button>
                        )}

                        {availableButtonSlugs.includes('quit') && (
                            <Button
                                onClick={() => emitButtonClick('quit')}
                                variant="destructive"
                                className="flex items-center gap-2 px-8 py-6 text-xl"
                                size="lg"
                            >
                                <X className="w-6 h-6" />
                                Quit
                            </Button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
