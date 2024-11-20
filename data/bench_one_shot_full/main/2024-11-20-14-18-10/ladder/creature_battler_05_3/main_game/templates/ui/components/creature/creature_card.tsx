import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as ShadcnCard, CardContent as ShadcnCardContent, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle } from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Progress = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnProgress>>(
  ({ uid, ...props }, ref) => <ShadcnProgress ref={ref} {...props} />
)

let Card = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnCard>>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnCardContent>>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnCardHeader>>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseProps & React.ComponentProps<typeof ShadcnCardTitle>>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

Progress.displayName = "Progress"
Card.displayName = "Card"
CardContent.displayName = "CardContent"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"

Progress = withClickable(Progress)
Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={uid}>
          <CardTitle uid={uid}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={uid}>
          <div className="flex flex-col gap-4">
            <img 
              src={image}
              alt={name}
              className="w-full h-[200px] object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{currentHp}/{maxHp}</span>
              </div>
              <Progress uid={uid} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
