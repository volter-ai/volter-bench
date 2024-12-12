import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  currentHp: number
  maxHp: number
  imageUrl: string
}

interface CustomCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CustomCard = withClickable(({ uid, ...props }: CustomCardProps) => (
  <Card {...props} />
))

let CustomCardHeader = withClickable(({ uid, ...props }: CustomCardProps) => (
  <CardHeader {...props} />
))

let CustomCardTitle = withClickable(({ uid, ...props }: CustomCardProps) => (
  <CardTitle {...props} />
))

let CustomCardContent = withClickable(({ uid, ...props }: CustomCardProps) => (
  <CardContent {...props} />
))

let CustomProgress = withClickable(({ uid, ...props }: CustomCardProps & { value: number }) => (
  <Progress {...props} />
))

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, currentHp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <CustomCard uid={`${uid}-card`} ref={ref} className={cn("w-[250px]", className)} {...props}>
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`} className="grid gap-4">
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
          <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span>HP</span>
              <span>{currentHp}/{maxHp}</span>
            </div>
            <CustomProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
