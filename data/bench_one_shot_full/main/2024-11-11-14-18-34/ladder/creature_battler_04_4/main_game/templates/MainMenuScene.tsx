import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface GameStats {
    [key: string]: number | undefined;
}

interface GameMeta {
    prototype_id?: string;
    category?: string;
    [key: string]: string | undefined;
}

interface BaseEntity {
    __type: string;
    stats: GameStats;
    meta: GameMeta;
    entities: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name?: string;
    description?: string;
}

interface Player extends BaseEntity {
    __type: 'Player';
}

interface GameUIData {
    entities: {
        player?: Player;
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    if (!props.data) {
        return (
            <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
                <div className="absolute inset-0 flex items-center justify-center bg-slate-900">
                    <p className="text-white">Loading...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
                {/* Title Section */}
                <Card className="w-full max-w-2xl bg-slate-800/50 backdrop-blur">
                    <div className="flex-1 flex items-center justify-center p-8">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            GAME TITLE
                        </h1>
                    </div>
                </Card>

                {/* Button Section */}
                <Card className="w-full max-w-md bg-slate-800/50 backdrop-blur p-6">
                    <div className="flex flex-col gap-4">
                        {availableButtonSlugs.length === 0 ? (
                            <p className="text-center text-white">No actions available</p>
                        ) : (
                            <>
                                {availableButtonSlugs.includes('play') && (
                                    <Button
                                        variant="default"
                                        size="lg"
                                        onClick={() => emitButtonClick('play')}
                                        className="w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700"
                                    >
                                        <Play className="w-6 h-6" />
                                        Play Game
                                    </Button>
                                )}

                                {availableButtonSlugs.includes('quit') && (
                                    <Button
                                        variant="destructive"
                                        size="lg"
                                        onClick={() => emitButtonClick('quit')}
                                        className="w-full flex items-center justify-center gap-2"
                                    >
                                        <XCircle className="w-6 h-6" />
                                        Quit
                                    </Button>
                                )}
                            </>
                        )}
                    </div>
                </Card>
            </div>
        </div>
    );
}
